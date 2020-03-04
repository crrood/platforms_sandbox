// js utilities
import * as common from "./common.js";

// query Adyen for up to date details on stored entities
document.querySelector("#refreshBtn").addEventListener("click", () => {
  common.AJAXGet(
     common.SERVER_URL + "/refresh",
     handleRefreshCallback
  );
})

// refresh displayed data on client
function handleRefreshCallback(data) {
  globals.accountHoldersList = data.accountHoldersList;
  globals.accountsList = data.accountsList;
  globals.updateAccountHolders();

  // display raw results
  globals.accountHoldersList.map(accountHolder =>
    common.output(accountHolder, "/getAccountHolder")
  )
  data.accountHolderBalancesList.map(accountHolderBalance =>
    common.output(accountHolderBalance, "/accountHolderBalance")
  )
}
