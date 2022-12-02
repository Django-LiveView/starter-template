import { Controller } from "../vendors/stimulus.js";
import { sendData } from "../webSocketsCli.js";
import { getLang } from "../mixins/miscellaneous.js";

export default class extends Controller {
  open(event) {
    const slug = event.currentTarget.dataset.slug;
    sendData({action: `Change page blog single - ${getLang()} - ${slug}`, data: {"slug": slug}});
  };

  nextPage(event) {
    const nextPage = event.currentTarget.dataset.nextPage;
    sendData({action: `Change to the next blog page - ${getLang()} - ${nextPage}`, data: {"page": nextPage}});
    sendData({action: `Update blog next button - ${getLang()} - ${nextPage}`, data: {"next_page": nextPage}});
  };
}
