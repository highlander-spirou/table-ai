import { observeResponseHandler, observerFactory } from "./src/oberver"

const observeResponse = observerFactory(document.getElementById("response"), observeResponseHandler)