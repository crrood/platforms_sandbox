// js utilities
import * as common from "./common.js";

document.querySelector("#refreshBtn").addEventListener("click", () => {
  common.AJAXGet(
     "http://localhost:5000/refresh",
     handleRefreshCallback
  );
})


function handleRefreshCallback(data) {
  // location.reload();
  console.log("refreshed");
  globals.updateAccountHolders(["updated!"]);
}
