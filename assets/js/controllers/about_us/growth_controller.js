import { Controller } from "../../vendors/stimulus.js";

let isDesktopview = false;

export default class extends Controller {
  static targets = [
    "description",
    "item"
  ];

  static values = { index: Number }

  closeDescription() {
    if (isDesktopview) {
      this.descriptionTargets.map((el) => {
        el.removeAttribute("style");
        el.parentElement.removeAttribute("style");
      });
    }
  };

  openDescription(event) {
    if (isDesktopview) {
      this.closeDescription();
      const height = `${this.descriptionTargets[event.params.index].scrollHeight}px`;
      this.descriptionTargets[event.params.index].style.height = height;
      this.descriptionTargets[event.params.index].parentElement.style.height = height;
    }
  };

  toggleDescription(event) {
    if (isDesktopview) {
      if (this.descriptionTargets[event.params.index].hasAttribute("style")) {
        this.closeDescription();
      } else {
        this.closeDescription();
        const height = `${this.descriptionTargets[event.params.index].scrollHeight}px`;
        this.descriptionTargets[event.params.index].style.height = height;
        this.descriptionTargets[event.params.index].parentElement.style.height = height;
      }
    }
  };

  descriptionTargetConnected() {
    isDesktopview = document.body.clientWidth > 900;

    window.onresize = () => {
      isDesktopview = document.body.clientWidth > 900;
      this.closeDescription();
    }
  };

  scrollNext(event) {
    event.preventDefault();

    const nextEl = this.itemTargets[event.params.next];

    nextEl?.parentNode.scrollTo({
      left: nextEl?.offsetLeft,
      behavior: "smooth"
    });
  };
  scrollPrev(event) {
    event.preventDefault();

    const prevEl = this.itemTargets[event.params.prev];

    prevEl?.parentNode.scrollTo({
      left: prevEl?.offsetLeft,
      behavior: "smooth"
    });
  };
}
