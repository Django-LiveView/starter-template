import { Controller } from "../vendors/stimulus.js";
import { sendData } from "../webSocketsCli.js";
import { getLang } from "../mixins/miscellaneous.js";

export default class extends Controller {

    static targets = ["name", "email", "message"];

    send(event) {
	event.preventDefault();
	sendData(
	    {
		action: "contact->send",
		data: {
		    name: this.nameTarget.value,
		    email: this.emailTarget.value,
		    message: this.messageTarget.value,
		}
	});
    }
}
