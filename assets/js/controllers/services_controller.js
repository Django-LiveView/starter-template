import { Controller } from "../vendors/stimulus.js";

export default class extends Controller {

  scrollToCategory(event) {
    event.preventDefault();

    const section = document.querySelector(event.params.anchor);
    if (section)
      section.scrollIntoView({ behavior: "smooth" });
  };

}
