import { Controller } from "../vendors/stimulus.js";
import { sendData } from "../webSocketsCli.js";
import { getLang } from "../mixins/miscellaneous.js";

export default class extends Controller {

    static targets = ["name", "email", "message", "isAcceptTerms"];

    send(event) {
	event.preventDefault();
	sendData(
	    {
		action: "contact->send_message",
		data: {
		    name: this.nameTarget.value,
		    email: this.emailTarget.value,
		    message: this.messageTarget.value,
		    is_accept_terms: this.isAcceptTermsTarget.checked,
		}
	});
    }
}
