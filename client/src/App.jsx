import React from "react"
import Map from './map/Map'

import { TransportProvider } from "./context/TransportProvider";

import "./App.css"
import Modal from "./misc/Modal";

export default function App() {
  return (
    <TransportProvider>
      <Modal/>
      <Map/>
    </TransportProvider>
  );
}