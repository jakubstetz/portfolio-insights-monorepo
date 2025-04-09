import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import Header from './Header/Header'
import ChartArea from './ChartArea/ChartArea'
import AlertsArea from './AlertsArea/AlertsArea'

function App() {
  return (
    <>
      <Header />
      <div id='main-area'>
        <ChartArea />
        <AlertsArea />
      </div>
    </>
  )
}

export default App