import { Controller } from "../vendors/stimulus.js";
import { sendData } from "../webSocketsCli.js";
import { getLang } from "../mixins/miscellaneous.js";

export default class extends Controller {

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

}
