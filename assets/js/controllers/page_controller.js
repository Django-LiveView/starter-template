import { Controller } from "../vendors/stimulus.js";
import { sendData } from "../webSocketsCli.js";
import { getLang } from "../mixins/miscellaneous.js";

export default class extends Controller {

  changePage(event) {
    event.preventDefault();
    const data = Object.assign({},
      event.currentTarget.dataset.scroll
        ? {"scroll": event.currentTarget.dataset.scroll}
        : {}
    );
    sendData({action: `${event.currentTarget.dataset.page}->send_page`, data: data});
  };
}
