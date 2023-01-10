import { Controller } from "../vendors/stimulus.js";
import { sendData } from "../webSocketsCli.js";
import { getLang, encodeFileAsBase64URL } from "../mixins/miscellaneous.js";

export default class extends Controller {

    static targets = ["avatar"];

    async updateAvatar(event) {
	// Get: data:image/jpeg;base64,[long string]
	const base64URL = await encodeFileAsBase64URL(this.avatarTarget.files[0]);
	const base64 = base64URL.split(',')[1];
	const mimeType = base64URL.split(';')[0].split(':')[1];
	sendData(
	    {
		action: "profile->update_avatar",
		data: {
		    base64: base64,
		    mimeType: mimeType
		}
	});
    }
}
