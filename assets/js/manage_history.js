// Imports
import { renderHtml } from "./mixins/miscellaneous.js";

export const manageHistory = () => {
  // Event listener for each time history changes occur
  window.onpopstate = (e) => {
    // Get user history list form local storage
    const data = e.target.localStorage.getItem(globalThis.userHistoryName)?.length > 0
      ? JSON.parse(e.target.localStorage.getItem(globalThis.userHistoryName))
      : null;

    // Get only previous route
    const dataToRender = data
      ? data[data.length - 2]
      : null;

    if (dataToRender) {
      // Renders the HTML received from the localStorage
      renderHtml(dataToRender, true);
      // Delete last route from array
      data.pop();
      // Update history list
      globalThis.historyList = data;
      // Update localStorage
      window.localStorage.setItem(globalThis.userHistoryName, JSON.stringify(data));
    } else if (data) {
      // Update URL
      history.pushState({}, "", data[0]?.url);
    }
  };
}
