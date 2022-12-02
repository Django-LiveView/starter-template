import { Controller } from "../../vendors/stimulus.js";

const slideUp = "slide-up";
const slideDown = "slide-down";
let scrollStatus = false;
let scrollEnabled = false;
let scrollTimer = 0;
let touchStartPosition = 0;

export default class extends Controller {
  static targets = [
    "teamGroup",
    "prev",
    "next",
    "currentPage",
    "totalPages"
  ];

  static values = { index: Number }

  connect() {
    this.totalPagesTarget.innerHTML = this.teamGroupTargets.length;
    this.currentPage();
    this.prevTarget.disabled = !this.hasPrevPage();
    this.nextTarget.disabled = !this.hasNextPage();
  };

  // get first touch position for mobile devices
  getTouchStartPosition(event) {
    if (event.changedTouches) touchStartPosition = event.changedTouches[0].clientY;
  };

  // slide element on scroll/touch movement
  slideTeamMembers(event) {
    event.preventDefault();

    const isScrollUp = event.changedTouches
      ? touchStartPosition < event.changedTouches[0].clientY
      : event.deltaY < 0;
    const isScrollDown = event.changedTouches
      ? touchStartPosition > event.changedTouches[0].clientY
      : event.deltaY > 0;
    const scrollAmount = isScrollDown ? 100 : -100;

    if (!scrollStatus) {
      if (isScrollDown) {
        if (this.hasNextPage()) {
          this.goToNextPage();
        } else {
          scrollEnabled = true;
        }
      }
      if (isScrollUp) {
        if (this.hasPrevPage()) {
          this.goToPrevPage();
        } else {
          scrollEnabled = true;
        }
      }

      scrollStatus = true;
    }

    clearInterval(scrollTimer);

    if (scrollEnabled) {
      window.scrollBy({
        top: scrollAmount,
        behavior: 'smooth'
      });
    } else {
      event.currentTarget.scrollIntoView({
        block: 'center',
        behavior: 'smooth'
      });
    }

    scrollTimer = setTimeout(() => {
      scrollStatus = false;
    }, 200);
  };

  // manage change page
  goToPrevPage() {
    this.teamGroupTargets[this.indexValue].classList.add(slideDown);
    this.indexValue--;
    this.teamGroupTargets[this.indexValue].classList.remove(slideUp);
    this.prevTarget.disabled = !this.hasPrevPage();
    this.nextTarget.disabled = !this.hasNextPage();
    this.currentPage();
  };
  goToNextPage() {
    this.teamGroupTargets[this.indexValue].classList.add(slideUp);
    this.indexValue++;
    this.teamGroupTargets[this.indexValue].classList.remove(slideDown);
    this.prevTarget.disabled = !this.hasPrevPage();
    this.nextTarget.disabled = !this.hasNextPage();
    this.currentPage();
  };

  // check pages availability
  hasNextPage() {
    return this.indexValue < this.teamGroupTargets.length - 1;
  };
  hasPrevPage() {
    return this.indexValue > 0;
  };

  // set current page
  currentPage() {
    this.currentPageTarget.innerHTML = this.indexValue + 1;
  }
}
