import { Controller } from "../vendors/stimulus.js";
import { sendData } from "../webSocketsCli.js";
import { removeBodyScrollLock, addBodyScrollLock } from "../mixins/miscellaneous.js";


const openClass = "open";

export default class extends Controller {

  static targets = [
    "isFooter",
    "name",
    "email",
    "phone",
    "message",
    "isAcceptTerms",
    "modal",
    "submit",
    "hcaptchaKey",
  ];

  modalTargetConnected(item) {
    setTimeout(() => {
      item.classList.add(openClass);
    }, 350);
    addBodyScrollLock();
  };

  closeModal() {
    this.modalTarget.classList.remove(openClass);
    removeBodyScrollLock();
  }

  sendForm(event) {
    event.preventDefault();

    // My HCaptcha
    const widgetID = hcaptcha.render(this.submitTarget, { sitekey:  this.hcaptchaKeyTarget.value });

    hcaptcha.execute(widgetID, { async: true })
      .then(({ response, key })=> {
        /***
         *
         *
         * AQUÍ ANTES DE ENVIAR EL FORMULARIO HAY QUE COMPROBAR LA "RESPONSE" SI ES VALIDA
         *
         *
         */
        sendData({action: `Send contact message`, data: {
            "is_footer": this.isFooterTarget.value.toLowerCase() === "true",
            "name": this.nameTarget.value,
            "email": this.emailTarget.value,
            "phone": this.hasPhoneTarget ? this.phoneTarget.value : false,
            "message": this.hasMessageTarget ? this.messageTarget.value : false,
            "is_accept_terms": this.isAcceptTermsTarget.value.toLowerCase() === "on"
          }});
      })
      .catch(err => {
        // SHOW MESSAGE??
        console.error(err);
      });

  }

}
