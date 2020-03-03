// React components
function AccountHolders(props) {
  return (
    props.accountHoldersList.map(accountHolder =>
        <AccountHolder key={accountHolder.accountHolderCode} accountHolderData={accountHolder} />
    )
  );
}

function AccountHolder(props) {
  const accounts = props.accountHolderData.accounts.map(accountData =>
    <Account key={accountData.accountCode} accountData={accountData} />
  )
  return (
    <div className="account-holder">
      <h2>{props.accountHolderData.accountHolderCode}</h2>
      <div className="account-holder__property"><b>Entity type:</b> {props.accountHolderData.legalEntity}</div>
      <div className="account-holder__property"><b>Status:</b> {props.accountHolderData.accountHolderStatus.status}</div>
      <div className="account-holder__property"><b>Payouts allowed:</b> {props.accountHolderData.accountHolderStatus.payoutState.allowPayout.toString()}</div>
      <h3>Accounts:</h3>
      {accounts}
    </div>
  );
}

// <div className="account-holder__property"><b>Events:</b> {props.accountHolderData.accountHolderStatus.events}</div>

function Account(props) {
  const accountData = globals.accountsList[props.accountData.accountCode];
  return (
    <div className="account">
      <div className="account__property"><b>Account code:</b> {accountData.accountCode}</div>
      <div className="account__property"><b>Description:</b> {accountData.description}</div>
      <div className="account__property"><b>Status:</b> {accountData.status}</div>
      <div className="account__property"><b>Balance:</b> {accountData.detailBalance.balance}</div>
      <div className="account__property"><b>On-hold balance:</b> {accountData.detailBalance.onHoldBalance}</div>
      <div className="account__property"><b>Pending balance:</b> {accountData.detailBalance.pendingBalance}</div>
    </div>
  )
}

// re-render after refresh
globals.updateAccountHolders = () => {
  ReactDOM.render(
    <AccountHolders accountHoldersList={globals.accountHoldersList} />,
    document.querySelector("#accountHoldersNode")
  )
}

// render on page load
window.onLoad = globals.updateAccountHolders();
