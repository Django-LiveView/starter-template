import { Controller } from "../vendors/stimulus.js";
import { sendData } from "../webSocketsCli.js";
import {
  removeBodyScrollLock,
  addBodyScrollLock,
  getLang
} from "../mixins/miscellaneous.js";

const openClass = "open";

export default class extends Controller {
  static targets = [
    "langMenu",
    "langList",
    "mobileMenu"
  ];

  toggleLangMenu() {
    this.langMenuTarget.classList.toggle(openClass);
    if (this.langMenuTarget.classList.contains(openClass)) {
      this.langListTarget.style.height = `${this.langListTarget.scrollHeight}px`;
      this.langListTarget.style.width = `${this.langListTarget.scrollWidth}px`;
      setTimeout(() => {
        this.langListTarget.style.height = "auto";
        this.langListTarget.style.width = "max-content";
      }, 300)
    } else {
      this.langListTarget.style.height = `${this.langListTarget.scrollHeight}px`;
      this.langListTarget.style.width = `${this.langListTarget.scrollWidth}px`;
      setTimeout(() => {
        this.langListTarget.style.height = "0px";
      }, 1);
      setTimeout(() => {
        this.langListTarget.style.width = "0px";
      }, 310);
    };
  };

  toggleMobileMenu() {
    this.mobileMenuTarget.classList.toggle(openClass);
    this.mobileMenuTarget.classList.contains(openClass)
      ? addBodyScrollLock()
      : removeBodyScrollLock();
  }

  changePage(event) {
    event.preventDefault();
    sendData({action: `Change page ${event.currentTarget.dataset.page} - ${getLang()}`, data: {}});
    this.mobileMenuTarget.classList.remove(openClass);
    removeBodyScrollLock();
  }
}
