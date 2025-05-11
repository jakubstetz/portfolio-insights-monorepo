package main

// Built-in Go packages
import (
	"encoding/json" // For converting structs to JSON (and vice versa)
	"fmt"           // For string formatting
	"io"            // For reading from response bodies
	"log"           // For printing logs to the terminal
	"net/http"      // For making and serving HTTP requests
	"os"            // For reading environment variables
	"github.com/joho/godotenv"	// For loading a .env file
)

// TiingoPrice represents a single entry from the Tiingo historical price API
// Note that keys are in PascalCase since we want to export them
type TiingoPrice struct {
	Date  string  `json:"date"`
	Close float64 `json:"close"`
}

// PriceResponse is what our Go service returns to the frontend/backend
type PriceResponse struct {
	Ticker string        `json:"ticker"`
	Prices []TiingoPrice `json:"prices"`
}

func init() {
	err := godotenv.Load()
	if err != nil {
		log.Println("⚠️  No .env file found — skipping.")
	}
}

func main() {
	// Define /stocks route
	// Note that * is the Go pointer operator
	http.HandleFunc("/stocks", func(w http.ResponseWriter, r *http.Request) {
		// Extract queries from GET request
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
		url := fmt.Sprintf("https://api.tiingo.com/tiingo/daily/%s/prices?token=%s", ticker, apiKey)
		resp, err := http.Get(url)
		if err != nil || resp.StatusCode != 200 {
			http.Error(w, "error fetching from Tiingo", http.StatusBadGateway)
			return
		}
		// "defer" schedules a function to run after the current function finishes
		defer resp.Body.Close()

		// Extract and format information from price history retrieval
		body, _ := io.ReadAll(resp.Body)

		var tiingoPrices []TiingoPrice
		json.Unmarshal(body, &tiingoPrices)

		response := PriceResponse{
			Ticker: ticker,
			Prices: tiingoPrices,
		}
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(response)
	})

	// Start server
	log.Println("🌐 Go Market Service running on :8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
