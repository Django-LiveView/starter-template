// Get lang
export function getLang() {
  return document.querySelector('html').getAttribute("lang");
}

// Prevent body scroll
export function addBodyScrollLock() {
  document.body.classList.add("scroll-lock");
}
export function removeBodyScrollLock() {
    document.body.classList.remove("scroll-lock");
}

export async function encodeFileAsBase64URL(file) {
    if (file) {
	return new Promise((resolve) => {
            const reader = new FileReader();
            reader.addEventListener('loadend', () => {
		resolve(reader.result);
            });
            reader.readAsDataURL(file);
	});
    }
    return null;
}

// The parallax function
export function parallax(el, x, y) {
    if (el) {
    const a = window.innerHeight - el.getBoundingClientRect().top
    el.style.transform = `translate3d(${x * a}px, ${y * a}px, 0)`;
  }
}

// Go to the top page
function scrollToTop () {
    window.scrollTo( {
        top: 0,
        behavior: "smooth",
    });
}

// Renders the HTML received from the Consumer or from indexedDB
export const renderHtml = (data, isBackward = false, isCachingData = false) => {
  const newFragmentHtml = document.createRange().createContextualFragment(data.html);

  const newFragmentHeader = document.createRange().createContextualFragment(data.header);
  const newFragmentMain = document.createRange().createContextualFragment(data.main);
  const newFragmentFooter = document.createRange().createContextualFragment(data.footer);

  const targetHtml = document.querySelector(data.selector);

  const targetHeader = document.querySelector("#content-header");
  const targetMain = document.querySelector("#main");
  const targetFooter = document.querySelector("#content-footer");

  if (targetHtml) {
    if (data.append) {
      targetHtml.appendChild(newFragmentHtml);
    } else {
      // Send data from Local Storage
      if (isBackward || isCachingData) {
        targetHeader.replaceChildren(newFragmentHeader);
        // Clear calendly iframe content, it will be generated automatically by its url
        if (data.action.includes("contact")) newFragmentMain.querySelector("#calendly").textContent = "";
        targetMain.replaceChildren(newFragmentMain);
        targetFooter.replaceChildren(newFragmentFooter);
      } else {
        targetHtml.replaceChildren(newFragmentHtml);
      }
    }

    // If it is a new page or is backward, the scroll returns to the beginning
    if ( data.html && !data.scroll && data.url || isBackward ) {
      setTimeout(() => { scrollToTop() }, 50);
    }

  } else {
    console.error(`Target ${data.selector} not found`);
    return;
  }
    // Update URL
    if (data.url) {
	window.history.pushState({ url: data.url }, "", data.url);
    }

    // Update title
    if (data.title) {
	document.title = data.title;
    }
}

export function moveScrollToAnchor(data) {
  if (data.scroll) {
    setTimeout(() => {
      document.querySelector(data.scroll).scrollIntoView({ behavior: "smooth" });
    }, 50)
  }
}
