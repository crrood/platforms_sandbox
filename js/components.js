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
  const events = props.accountHolderData.accountHolderStatus.events.map((eventData, i) =>
    <Event key={props.accountHolderData.accountHolderCode + "Event" + i} eventData={eventData} />
  )
  return (
    <div className="pane account-holder">
      <h2>{props.accountHolderData.accountHolderCode}</h2>
      <div className="account-holder__property"><b>Entity type:</b> {props.accountHolderData.legalEntity}</div>
      <div className="account-holder__property"><b>Status:</b> {props.accountHolderData.accountHolderStatus.status}</div>
      <div className="account-holder__property"><b>Payouts allowed:</b> {props.accountHolderData.accountHolderStatus.payoutState.allowPayout.toString()}</div>
      <div className="account-holder__property"><b>Events: </b><br/>
        {events}
      </div>
      <h3>Accounts:</h3>
        {accounts}
    </div>
  );
}

function Event(props) {
  return (
    <div className="event">
      <div className="event__property"><b>Type: </b>{props.eventData.event}</div>
      <div className="event__property"><b>Execution Date: </b>{props.eventData.executionDate}</div>
      <div className="event__property"><b>Reason: </b>{props.eventData.reason}</div>
    </div>
  )
}

function Account(props) {
  const accountData = globals.accountsList[props.accountData.accountCode];
  const [balance, onHoldBalance, pendingBalance] = ["balance", "onHoldBalance", "pendingBalance"].map(balanceType =>
    <BalanceDetail key={accountData.accountCode + balanceType} balanceData={accountData.detailBalance[balanceType]} />
  )
  return (
    <div className="account">
      <div className="account__property"><b>Account code:</b> {accountData.accountCode}</div>
      <div className="account__property"><b>Description:</b> {accountData.description}</div>
      <div className="account__property"><b>Status:</b> {accountData.status}</div>
      <div className="account__property"><b>Balance:</b> {balance}</div>
      <div className="account__property"><b>On-hold balance:</b> {onHoldBalance}</div>
      <div className="account__property"><b>Pending balance:</b> {pendingBalance}</div>
    </div>
  )
}

function BalanceDetail(props) {
  const balanceList = props.balanceData.map(currencyBalance =>
    <div className="balance">
      {parseInt(props.balanceData.value) / 100} {props.balanceData.currency}
    </div>
  )
  return (
    props.balanceData.map(currencyBalance =>
      <div className="balance">
        {currencyBalance.value.toString().slice(0, -2) + "." + currencyBalance.value.toString().slice(-2)} {currencyBalance.currency}
      </div>
    )
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
