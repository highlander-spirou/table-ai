import {observerFactory, observeResponseHandler} from '../src/oberver'

const node = document.getElementById('response')

observerFactory(node, observeResponseHandler)