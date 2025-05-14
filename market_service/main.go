/*
main.go starts an HTTP server that proxies stock data from Tiingo.

Comments in this file are intentionally verbose for educational purposes.
This is my first time writing a full Go file as part of a larger project,
so I was liberal—even excessive—with comments to facilitate learning and
to serve as a reference for future Go development.
*/

package main // Every standalone executable Go program must have package main

// Built-in Go packages
import (
	"encoding/json"            // For converting structs to JSON (and vice versa)
	"fmt"                      // For string formatting
	"github.com/joho/godotenv" // For loading a .env file
	"io"                       // For reading from response bodies
	"log"                      // For printing logs to the terminal
	"net/http"                 // For making and serving HTTP requests
	"os"                       // For reading environment variables
	"strconv"                  // For converting strings to numbers (e.g. price query param to float)
)

// PricePoint represents a single entry from the Tiingo historical price API
// Note that fields are in PascalCase since we want to export them
// Note that JSON object keys map to Go struct fields
type PricePoint struct {
	Date  string  `json:"date"`  // Struct tag for JSON marshalling/unmarshalling
	Close float64 `json:"close"` // Field must be exported (capitalized) to be included in JSON
}

// PriceResponse is what our Go service returns to the frontend/backend
// when returning stock price historical data
type PriceResponse []PricePoint

// LastPrice is used in our alert validation endpoint to store the most
// recent stock price
type LastPrice struct {
	Last      *float64 `json:"last"` // Pointer used to check if value exists in /check-alert implementation
	PrevClose float64  `json:"prevClose"`
}

// Load .env file
func init() {
	// init runs automatically before main.
	err := godotenv.Load()
	if err != nil {
		log.Println("⚠️  No .env file found — skipping.")
	}
}

func main() {
	// --------- Health Check ---------

	// Define /health-check route
	// This verifies that the Go microservice is running and that it is connected to the Tiingo API
	http.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
		apiKey := os.Getenv("TIINGO_API_KEY")
		if apiKey == "" {
			http.Error(w, "missing API key", http.StatusInternalServerError)
			return
		}

		// Make lightweight request to Tiingo using stable ticker (SPY)
		url := fmt.Sprintf("https://api.tiingo.com/tiingo/daily/SPY/prices?token=%s", apiKey)
		resp, err := http.Get(url)
		if err != nil || resp.StatusCode != 200 {
			http.Error(w, "error fetching from Tiingo", http.StatusBadGateway)
			return
		}
		defer resp.Body.Close() // Clean up response body

		// Confirm service and API connectivity
		w.WriteHeader(http.StatusOK)
		w.Write([]byte(`{"health": true}`))
	})

	// --------- Stock Data Retrieval ---------

	// Define /stocks route
	// Note that * is the Go pointer operator
	// w and r are analogous to res and req in Express.js, respectively
	http.HandleFunc("/stocks", func(w http.ResponseWriter, r *http.Request) {
		// Extract queries from GET request
		// Go idiom: := declares and initializes a variable with inferred type
		ticker := r.URL.Query().Get("ticker")
		startDate := r.URL.Query().Get("startDate")
		resampleFreq := r.URL.Query().Get("interval")

		if ticker == "" || startDate == "" || resampleFreq == "" {
			http.Error(w, "missing query parameter", http.StatusBadRequest)
			return
		}

		// Load in Tiingo API key
		apiKey := os.Getenv("TIINGO_API_KEY")
		if apiKey == "" {
			http.Error(w, "missing API key", http.StatusInternalServerError)
			return
		}

		// Send GET request to Tiingo API to retrieve stock price history
		url := fmt.Sprintf(
			"https://api.tiingo.com/tiingo/daily/%s/prices?startDate=%s&resampleFreq=%s&token=%s",
			ticker,
			startDate,
			resampleFreq,
			apiKey,
		)
		resp, err := http.Get(url)
		// OK response is expected to have no error and a 200 status code
		if err != nil || resp.StatusCode != 200 {
			http.Error(w, "error fetching from Tiingo", http.StatusBadGateway)
			return
		}
		// "defer" schedules a function to run after the current function finishes
		defer resp.Body.Close() // Ensures the response body is closed when this function ends

		// Extract and format information from price history retrieval
		// As in other languages, _ is used to indicate an unused variable
		body, _ := io.ReadAll(resp.Body)

		var tiingoPrices []PricePoint
		// Unmarshalling converts JSON bytes into native Go data structures
		// Error is ignored here for brevity, but should be handled in production.
		// &tiingoPrices passes a pointer so json.Unmarshal can populate the slice in place
		json.Unmarshal(body, &tiingoPrices)
		w.Header().Set("Content-Type", "application/json") // Set headers
		json.NewEncoder(w).Encode(tiingoPrices)            // Format as JSON
	})

	// --------- New Alert Validity Check ---------

	http.HandleFunc("/check-alert", func(w http.ResponseWriter, r *http.Request) {
		ticker := r.URL.Query().Get("ticker")
		priceStr := r.URL.Query().Get("price")
		direction := r.URL.Query().Get("direction")

		if ticker == "" || priceStr == "" || direction == "" {
			http.Error(w, "missing query parameter", http.StatusBadRequest)
			return
		}

		price, err := strconv.ParseFloat(priceStr, 64)
		if err != nil {
			http.Error(w, "invalid price", http.StatusBadRequest)
			return
		}

		apiKey := os.Getenv("TIINGO_API_KEY")
		if apiKey == "" {
			http.Error(w, "missing API key", http.StatusInternalServerError)
			return
		}

		url := fmt.Sprintf("https://api.tiingo.com/iex/%s?token=%s", ticker, apiKey)
		resp, err := http.Get(url)
		if err != nil || resp.StatusCode != 200 {
			http.Error(w, `{"valid": false, "message": "Ticker not found or data unavailable."}`, http.StatusBadRequest)
			return
		}
		defer resp.Body.Close()

		body, _ := io.ReadAll(resp.Body)
		var result []LastPrice
		json.Unmarshal(body, &result)
		// Verify price data has been successfully retrieved
		if err != nil {
			http.Error(w, `{"valid": false, "message": "Ticker not found."}`, http.StatusInternalServerError)
			return
		}
		if len(result) == 0 {
			http.Error(w, `{"valid": false, "message": "Ticker not found."}`, http.StatusBadRequest)
			return
		}

		// Use last price if it exists (i.e. market is open)
		// Use Previous close otherwise (i.e. market is closed)
		var currentPrice float64
		if result[0].Last != nil {
			currentPrice = *result[0].Last
		} else {
			currentPrice = result[0].PrevClose
			log.Printf(`⚠️  Live price unavailable for %s — using previous close.`, ticker)
		}

		// Set header preemptively rather than repeating for each possible JSON response
		w.Header().Set("Content-Type", "application/json")

		// Check for invalid alert
		if (direction == "below" && currentPrice < price) || (direction == "above" && currentPrice > price) {
			msg := fmt.Sprintf("Current price is $%.2f, already %s $%.2f.", currentPrice, direction, price)
			http.Error(w, fmt.Sprintf(`{"message": "%s"}`, msg), http.StatusBadRequest)
			return
		}

		// Valid alert
		json.NewEncoder(w).Encode(map[string]interface{}{
			"valid":   true,
			"message": "Valid alert.",
		})
	})

	// --------- Start Server ---------

	// Start server
	log.Println("🌐 Go Market Service running on :8080")
	// Start HTTP server on port 8080. nil means default ServeMux is used.
	log.Fatal(http.ListenAndServe(":8080", nil))
}
