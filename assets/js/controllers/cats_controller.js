import { Controller } from "../vendors/stimulus.js";
import { sendData } from "../webSocketsCli.js";
import { getLang, encodeFileAsBase64URL } from "../mixins/miscellaneous.js";

export default class extends Controller {

    static targets = ["name", "age", "biography", "avatar"];

    openCatSingle(event) {
	event.preventDefault();
	const slug = event.target.dataset.slug;
	sendData({action: "cat_single->send_page", data: {slug: slug}});
    }

    nextPage(event) {
	event.preventDefault();
	const data = Object.assign({},
				   event.currentTarget.dataset.pagination
				 ? {"pagination": event.currentTarget.dataset.pagination}
				 : {}
	);
	sendData({action: "cats->next_page", data: data});
    };

    previousPage(event) {
	event.preventDefault();
	const data = Object.assign({},
				   event.currentTarget.dataset.pagination
				 ? {"pagination": event.currentTarget.dataset.pagination}
				 : {}
	);
	sendData({action: "cats->previous_page", data: data});
    };

    async create(event) {
	event.preventDefault();
	// Get: data:image/jpeg;base64,[long string]
	const base64URL = await encodeFileAsBase64URL(this.avatarTarget.files[0]);
	const base64 = base64URL ? base64URL.split(',')[1] : false;
	const mimeType = base64URL ? base64URL.split(';')[0].split(':')[1] : false;
	sendData({action: "cat_new->create", data: {
	    form : {
		name: this.nameTarget.value,
		age: this.ageTarget.value,
		biography: this.biographyTarget.value,
		avatar: {
		    base64: base64,
		    mimeType: mimeType
		}
	    }
	}});
    };

    async openUpdateForm(event) {
	event.preventDefault();
	const slug = event.target.dataset.slug;
	sendData({action: "cat_update->send_page", data: {slug: slug}});
    };

    async update(event) {
	event.preventDefault();
	const slug = event.target.dataset.slug;
	// Get: data:image/jpeg;base64,[long string]
	const base64URL = await encodeFileAsBase64URL(this.avatarTarget.files[0]);
	const base64 = base64URL ? base64URL.split(',')[1] : false;
	const mimeType = base64URL ? base64URL.split(';')[0].split(':')[1] : false;
	sendData({action: "cat_update->update", data: {
	    slug: slug,
	    form : {
		name: this.nameTarget.value,
		age: this.ageTarget.value,
		biography: this.biographyTarget.value,
		avatar: {
		    base64: base64,
		    mimeType: mimeType
		}
	    }
	}});
    };

    async delete(event) {
	event.preventDefault();
	sendData({
	    action: "cats->delete",
	    data: {
		slug: event.currentTarget.dataset.slug
	    }
	});
    };
}
