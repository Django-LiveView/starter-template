// Imports
import {
  addBodyScrollLock,
  removeBodyScrollLock,
  renderHTML,
  moveScrollToAnchor
} from "./mixins/miscellaneous.js";

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
 * Send data to WebSockets server
 * @param {string} message
 * @param {WebSocket} webSocket
 * @return {void}
 */
export function sendData(message, webSocket=window.myWebSocket) {
    if (webSocket.readyState === WebSocket.OPEN) {
	// Add lang
	const messageWithoutLang = message;
	messageWithoutLang.data.lang = document.querySelector("html").getAttribute("lang");
	const messageFull = messageWithoutLang;
	// Send
	webSocket.send(JSON.stringify(messageFull));
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

  // Event when a new message is received by WebSockets
  webSocket.addEventListener("message", (event) => {
    // Parse the data received
      const data = JSON.parse(event.data);

    // Renders the HTML received from the Consumer
      renderHTML(data);
      moveScrollToAnchor(data);
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
