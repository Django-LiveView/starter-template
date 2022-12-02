// Imports
import {
  addBodyScrollLock,
  removeBodyScrollLock,
  renderHtml,
  moveScrollToAnchor
} from "./mixins/miscellaneous.js";

const DEBUG = document.body.dataset.debug === "True";

// Limit of routes to be stored
const LIMIT_ROUTES_CAN_SAVE = 50;

const minutesToClearHistoryList = DEBUG ? 0 : 60;

/*
   FUNCTIONS
 */

function showNoConnectionModal() {
    document.querySelector("#modal-no-connection")?.classList.add("show");
    document.querySelector("#modal-button-refresh-page")?.addEventListener('click', () => {
        location.reload();
    });
    addBodyScrollLock();
    setTimeout(() => {
        document.querySelector("#modal-no-connection-content")?.classList.remove("hide");
    }, 2000)
}

function hideNoConnectionModal() {
    document.querySelector("#modal-no-connection")?.classList.remove("show");
    document.querySelector("#modal-no-connection-content")?.classList.add("hide");
    removeBodyScrollLock();
}

/**
 * Connect to WebSockets server (SocialNetworkConsumer)
 * @param {string} url - WebSockets server url
 * @return {WebSocket}
 */
export function connect(url=`${'https:' == document.location.protocol ? 'wss' : 'ws'}://${ document.body.dataset.host }/ws/website/`) {
  console.log("Connecting to WebSockets server...");
    window.myWebSocket = new WebSocket(url);
    return window.myWebSocket;
}

/**
 * Clear Local Storage History List
 */
function clearLocalStorageHistoryList() {
  if (window.localStorage.getItem(globalThis.userHistoryName)) {
    globalThis.historyList = [];
    window.localStorage.setItem(globalThis.userHistoryName, "");
  }
}

/**
 * Push data to HISTORY LIST array
 */
function pushDataToHistoryListAndUpdateLocalStorage(data) {

  // add route to array
  globalThis.historyList.push(data);

  // update localStorage
  window.localStorage.setItem(globalThis.userHistoryName, JSON.stringify(globalThis.historyList));
}

/**
 * Function that adds in localstorage each route
 * @param data
 */
function addToLocalStorageHistoryList(data) {

  let dataDuplicated = data;

  if (data.html && data.url) {

    dataDuplicated = data;

    // Set Selectors
    dataDuplicated.selectorHeader = "header";
    dataDuplicated.selectorMain = "#main";
    dataDuplicated.selectorFooter = "div#content-footer";

    // Get HTML fragments
    dataDuplicated.header = document.querySelector('#content-header').innerHTML;
    dataDuplicated.main = document.querySelector('#main');
    if (dataDuplicated.action.includes("contact")) {
      dataDuplicated.main = dataDuplicated.main.innerHTML;
    } else {
      dataDuplicated.main = dataDuplicated.main.innerHTML;
    }
    setTimeout(()=> { dataDuplicated.footer = document.querySelector('#content-footer').innerHTML }, 100);
    dataDuplicated.append = false;
  }

  // If the limit has not been exceeded and the HTML and a URL exist, the data is added to the list of routes.
  if (globalThis.historyList.length < LIMIT_ROUTES_CAN_SAVE && data.html && data.url ) {

    pushDataToHistoryListAndUpdateLocalStorage(dataDuplicated);

  } else if ( globalThis.historyList.length === LIMIT_ROUTES_CAN_SAVE && data.html && data.url ) {

    // If the limit has been exceeded, the first half of the list is emptied
    globalThis.historyList = globalThis.historyList.slice((LIMIT_ROUTES_CAN_SAVE / 2), (LIMIT_ROUTES_CAN_SAVE + 1));

    pushDataToHistoryListAndUpdateLocalStorage(dataDuplicated);
  }
}

/***
 * Function for update seo tags
 * @param data
 */
function updateSeoTag(data) {

  // Set title
  const titleData = data.title
  const titleDefaultData = "CCSTech.io"
  if (titleData !== undefined) {
    if (titleData !== "") {
      document.querySelector("#title").textContent = titleData + titleDefaultData;
    } else {
      document.querySelector("#title").textContent = titleDefaultData;
    }
  }

}

/**
 * Send data to WebSockets server
 * @param {string} message
 * @param {WebSocket} webSocket
 * @return {void}
 */
export function sendData(message, webSocket=window.myWebSocket) {

  let cachingData;

  const dataFromLocalStorage = window.localStorage.getItem(globalThis.userHistoryName)?.length > 0
    ? JSON.parse(window.localStorage.getItem(globalThis.userHistoryName))
    : null;

  if (dataFromLocalStorage) cachingData = dataFromLocalStorage.filter((obj)=> obj.action === message.action);

  if (cachingData?.length > 0) {
    // Update seo tag
    updateSeoTag(cachingData[0])
    renderHtml(cachingData[0], false, true);
    moveScrollToAnchor(cachingData[0]);
    pushDataToHistoryListAndUpdateLocalStorage(cachingData[0]);
  } else {
    if (webSocket.readyState === WebSocket.OPEN) {
      webSocket.send(JSON.stringify(message));
    } else {
      setTimeout(() => {
        sendData(message);
      }, 100);
    }
  }
}

/*
    EVENTS
*/

/**
 * On WebSockets server connection
 * @param {WebSocket} webSocket
 * @return {void}
 */
export function startEvents(webSocket=window.myWebSocket) {

  globalThis.historyList = [];
  globalThis.userHistoryName = "user-history-ccstech";

  // Check if local Storage already exist and if the death time is expired
  if(window.localStorage.getItem(globalThis.userHistoryName)) {

    const deathTime = JSON.parse(window.localStorage.getItem(`${globalThis.userHistoryName}-death-time`));

    // If the death time has expired, the local storage will be cleared
    if (!deathTime || deathTime < new Date().valueOf()) {
      clearLocalStorageHistoryList();
      // Set Local Storage Death time
      window.localStorage.setItem(`${globalThis.userHistoryName}-death-time`, JSON.stringify((new Date().valueOf()) + (minutesToClearHistoryList * 60 * 1000)));
    }

  } else {
    // Set Local Storage Death time
    window.localStorage.setItem(`${globalThis.userHistoryName}-death-time`, JSON.stringify((new Date().valueOf()) + (minutesToClearHistoryList * 60 * 1000)));
  }

  // Interval to clear local storage
  setInterval(()=> {
    clearLocalStorageHistoryList();
  }, minutesToClearHistoryList * 60 * 1000)

  // Event when a new message is received by WebSockets
  webSocket.addEventListener("message", (event) => {
    // Parse the data received
    const data = JSON.parse(event.data);

    // Renders the HTML received from the Consumer
    updateSeoTag(data);
    renderHtml(data);
    moveScrollToAnchor(data);

    // Function that adds in localstorage each route
    addToLocalStorageHistoryList(data);
  });

  /**
   * Reconnect to WebSockets server
   * @param webSocket
   * @returns {boolean} - True if the connection was successful, false otherwise
   */
  function reconnect(webSocket=window.myWebSocket) {
    const statusConnection = webSocket.readyState === WebSocket.OPEN;
    if (!statusConnection) {
      webSocket.close();
      console.log("Reconnecting to WebSockets server...");
      connect();
    }
    return statusConnection;
  }

  webSocket.addEventListener("open", () => {
    hideNoConnectionModal();
    console.log("Connected to WebSockets server");
  });

  function showModalReconnect() {
    showNoConnectionModal();
    console.log("Connection closed with WebSockets server");
    reconnect();
  }

  // Lost connection with WebSockets server
  webSocket.addEventListener("error", showModalReconnect);
  webSocket.addEventListener("close", showModalReconnect);
  webSocket.addEventListener("closed", showModalReconnect);
  window.addEventListener('offline', showModalReconnect);
  window.addEventListener('online', hideNoConnectionModal);
}
