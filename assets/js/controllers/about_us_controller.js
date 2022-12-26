import { Controller } from "../vendors/stimulus.js";
import { sendData } from "../webSocketsCli.js";
import { getLang } from "../mixins/miscellaneous.js";

export default class extends Controller {

    static targets = [];

    getRandomNumberText(event) {
	sendData(
	    {
		action: "about_us->update_random_number_text",
		data: {}
	    }
	);
    }

    getRandomNumberHTML(event) {
	sendData(
	    {
		action: "about_us->update_random_number_html",
		data: {}
	    }
	);
    }
}
