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
    common.output(accountHolder, "/getAccountHolder", common.endpoints.getAccountHolder)
  )
  data.accountHolderBalancesList.map(accountHolderBalance =>
    common.output(accountHolderBalance, "/accountHolderBalance", common.endpoints.accountHolderBalance)
  )
}

// gather data from payment form and send to Adyen
function makeSplitPayment() {
  const splitAmount = parseInt(document.querySelector("#splitAmountInput").value);
  const commissionAmount = parseInt(document.querySelector("#commissionAmountInput").value);
  const request = {
    "amount": {
      "currency": "USD",
      "value": splitAmount + commissionAmount
    },
    "reference": "AfP Demo Split Payment",
    "paymentMethod": {
      "type": "scheme",
      "number": "4111111111111111",
      "expiryMonth": "03",
      "expiryYear": "2030",
      "holderName": "John Smith",
      "cvc": "737"
    },
    "splits": [
      {
        "amount": {
          "value": commissionAmount,
          "currency": "USD"
        },
        "type": "Commission",
        "reference": "Platform split"
      },
      {
        "amount": {
          "value": splitAmount,
          "currency": "USD"
        },
        "type": "MarketPlace",
        "account": document.querySelector("#splitAccountCodeInput").value,
        "reference": "Seller split"
      }
    ],
    "merchantAccount": ""
  }

  // URL to forward request to
  request.endpoint = common.endpoints.payments;

  common.AJAXPost(
    common.SERVER_URL + "/forwardRequest",
    handlePaymentsCallback,
    request
  )
}

function handlePaymentsCallback(data) {
  common.output(data.request, "/payments request", data.endpoint);
  common.output(data.response, "/payments response");
}

function doTransferFunds() {
  const request = {
  	destinationAccountCode: document.querySelector("#destinationAccountCodeInput").value,
  	sourceAccountCode: document.querySelector("#sourceAccountCodeInput").value,
  	amount: {
  		currency: document.querySelector("#transferCurrencyInput").value,
  		value: document.querySelector("#transferAmountInput").value
  	},
  	merchantReference: "AfP demo transfer",
  	transferCode: "CREDIT_EXAMPLE" // hardcoded value which is defined at Platform creation
  };

  // URL to send request to
  request.endpoint = common.endpoints.transferFunds;

  common.AJAXPost(
    common.SERVER_URL + "/forwardRequest",
    handleTransferFundsCallback,
    request
  )
}

function handleTransferFundsCallback(data) {
  common.output(data.request, "/transferFunds request", data.endpoint);
  common.output(data.response, "/tranferFunds response");
}

document.querySelector("#payBtn").addEventListener("click", makeSplitPayment);
document.querySelector("#transferFundsBtn").addEventListener("click", doTransferFunds);
