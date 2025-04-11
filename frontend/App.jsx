import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import Header from './Header/Header'
import ChartArea from './ChartArea/ChartArea'
import AlertsArea from './AlertsArea/AlertsArea'
import AlertCreationPrompt from './AlertCreationPrompt/AlertCreationPrompt'

function App() {
  const [showAlertCreationPrompt, setShowAlertCreationPrompt] = useState(false)

  return (
    <>
      <Header />
      <div id='main-area'>
        <ChartArea />
        <AlertsArea onNewAlert={() => setShowAlertCreationPrompt(true)}/>
      </div>
      {showAlertCreationPrompt && (
        <AlertCreationPrompt onClose={() => setShowAlertCreationPrompt(false)}/>
      )}
    </>
  )
}

export default App