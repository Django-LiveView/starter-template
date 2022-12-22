import { Controller } from "../vendors/stimulus.js";
import { sendData } from "../webSocketsCli.js";
import { getLang } from "../mixins/miscellaneous.js";

export default class extends Controller {

    static targets = ["email", "password"];

    logIn(event) {
	event.preventDefault();
	sendData(
	    {
		action: "login->log_in",
		data: {
		    email: this.emailTarget.value,
		    password: this.passwordTarget.value
		}
	});
    }

    logOut(event) {
	event.preventDefault();
	sendData(
	    {
		action: "login->log_out",
		data: {}
	});
	}
}
