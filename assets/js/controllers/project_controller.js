import { Controller } from "../vendors/stimulus.js";
import { sendData } from "../webSocketsCli.js";
import { getLang } from "../mixins/miscellaneous.js";

export default class extends Controller {

  open(event) {
    sendData({action: `Change page project single - ${getLang()} - ${event.currentTarget.dataset.slug}`, data: {
      "category": event.currentTarget.dataset.category,
      "slug": event.currentTarget.dataset.slug
    }});
  };

  openCategory(event) {
    const data = Object.assign({}, {
      "slug": event.currentTarget.dataset.slug,
      "scroll": event.currentTarget.dataset.scroll
    });
    sendData({
      action: `Change page projects category - ${getLang()} - ${event.currentTarget.dataset.slug}`,
      data: data
    });
  };

  nextPage(event) {
    const slug = event.currentTarget.dataset.slug;
    const nextPage = event.currentTarget.dataset.nextPage;
    sendData({action: "Change to the next category page", data: {
      "slug": slug,
      "nextPage": nextPage
    }});
  };

}
