// js utilities
import * as common from "./common.js";

// object to store global variables
const globals = {};

document.querySelector("#refreshBtn").addEventListener("click", () => {
  common.AJAXGet(
     "http://localhost:5000/refresh",
     handleRefreshCallback
  );
})


function handleRefreshCallback(data) {
  location.reload();
}
