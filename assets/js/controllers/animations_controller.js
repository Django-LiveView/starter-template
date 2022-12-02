import { Controller } from "../vendors/stimulus.js";

export default class extends Controller {
  connect() {

    const optionWholeElementIsVisible = { threshold: 1.0 };
    const playOnVisible = function(embedElement, svgID, iterations=1) {
      const svgDoc = embedElement?.contentDocument;
      const svgAnimation = svgDoc?.querySelector(svgID);
      const player = svgAnimation?.svgatorPlayer;
      player?.set("iterations", iterations).play();
    };

    // "Greeting Robot" at footer
    const greetingRobotEmbed = document.querySelector("#greeting-robot");

    // Set time interval "Greeting Robot" animation when loaded
    if (greetingRobotEmbed) {
      greetingRobotEmbed.addEventListener("load", () => {
        const player = this.animationPlayer(greetingRobotEmbed, "#eamvuZRe23f1");
        player.set("iterations", 1);
        setInterval(() => {
          player.play()
        }, 7500)
      }, false);
    }

    // "APP Robot"
    const homeAppRobotEmbed = document.querySelector("#app-robot");

    // Observe "APP Robot" to start animation when visible"
    const homeAppRobotIntersectionObserver = new IntersectionObserver(() => {
      playOnVisible(homeAppRobotEmbed, "#eueQxRYlTWw1");
    }, optionWholeElementIsVisible);

    // Stop "APP Robot" animation when loaded
    if (homeAppRobotEmbed) {
      homeAppRobotEmbed.addEventListener("load", () => {
        const player = this.animationPlayer(homeAppRobotEmbed, "#eueQxRYlTWw1");
        player.set("iterations", 1);

        homeAppRobotIntersectionObserver.observe(homeAppRobotEmbed);
      }, false);
    }

    // "Robotic Arm"
    const homeRoboticArmEmbed = document.querySelector("#robotic-arm");

    // Stop "Robotic Arm" animation when loaded
    if (homeRoboticArmEmbed) {
      homeRoboticArmEmbed.addEventListener("load", () => {
        const player = this.animationPlayer(homeRoboticArmEmbed, "#e8CdnGNchjk1");
        player.set("iterations", 1);
      }, false);

      // Observe "Robotic Arm" to start animation when visible"
      const homeRoboticArmIntersectionObserver = new IntersectionObserver(() => {
        playOnVisible(homeRoboticArmEmbed, "#e8CdnGNchjk1")
      }, optionWholeElementIsVisible);

      homeRoboticArmIntersectionObserver.observe(homeRoboticArmEmbed);
    }

    // "Home Web"
    const homeWebEmbed = document.querySelector("#home-web");

    // Stop "Home Web" animation when loaded
    if (homeWebEmbed) {
      homeWebEmbed.addEventListener("load", () => {
        const player = this.animationPlayer(homeWebEmbed, "#eI480oTXiG11");
        player.set("iterations", 1);
      }, false);
    }

    // "Home APP"
    const homeAppEmbed = document.querySelector("#home-app");

    // Stop "Home APP" animation when loaded
    if (homeAppEmbed) {
      homeAppEmbed.addEventListener("load", () => {
        const player = this.animationPlayer(homeAppEmbed, "#ecYdFQsEweL1");
        player.set("iterations", 1);
      }, false);
    }

    // "Home Platform"
    const homePlatformsEmbed = document.querySelector("#home-platforms");

    // Stop "Home Platform" animation when loaded
    if (homePlatformsEmbed) {
      homePlatformsEmbed.addEventListener("load", () => {
        const player = this.animationPlayer(homePlatformsEmbed, "#eOH8tu7D3sq1");
        player.set("iterations", 1);
      }, false);
    }


    // "CPU Robot"
    const aboutCpuRobotEmbed = document.querySelector("#cpu-robot");

    // Stop "CPU Robot" animation when loaded
    if (aboutCpuRobotEmbed) {
      aboutCpuRobotEmbed.addEventListener("load",() => {
        const player = this.animationPlayer(aboutCpuRobotEmbed, "#eeoJ694Blpv1");
        player.set("iterations", 1);
      }, false);

      // Observe "CPU Robot" to start animation when visible"
      const aboutCpuRobotIntersectionObserver = new IntersectionObserver(() => {
        playOnVisible(aboutCpuRobotEmbed, "#eeoJ694Blpv1");
      }, optionWholeElementIsVisible);

      aboutCpuRobotIntersectionObserver.observe(aboutCpuRobotEmbed);
    }


    // "About Mission"
    const aboutMissionEmbed = document.querySelector("#about-mission");

    // Stop "About Mission" animation when loaded
    if (aboutMissionEmbed) {
      aboutMissionEmbed.addEventListener("load", () => {
        const player = this.animationPlayer(aboutMissionEmbed, "#e8EHcZXn61D1");
        player.set("iterations", 1);
      }, false);

      // Observe "About Mission" to start animation when visible"
      const aboutMissionIntersectionObserver = new IntersectionObserver(() => {
        playOnVisible(aboutMissionEmbed, "#e8EHcZXn61D1");
      }, optionWholeElementIsVisible);

      aboutMissionIntersectionObserver.observe(aboutCpuRobotEmbed);
    }

    // "About Vision"
    const aboutVisionEmbed = document.querySelector("#about-vision");

    // Stop "About Vision" animation when loaded
    if (aboutVisionEmbed) {
      aboutVisionEmbed.addEventListener("load", () => {
        const player = this.animationPlayer(aboutVisionEmbed, "#eeaZ3kXhGVw1");
        player.set("iterations", 1);
      }, false);

      // Observe "About Vision" to start animation when visible"
      const aboutVisionIntersectionObserver = new IntersectionObserver(() => {
        playOnVisible(aboutVisionEmbed, "#eeaZ3kXhGVw1");
      }, optionWholeElementIsVisible);

      aboutVisionIntersectionObserver.observe(aboutVisionEmbed);
    }

    // "About OpenSource"
    const aboutOpenSourceEmbed = document.querySelector("#about-open-source");

    // Stop "About OpenSource" animation when loaded
    if (aboutOpenSourceEmbed) {
      aboutOpenSourceEmbed.addEventListener("load", () => {
        const player = this.animationPlayer(aboutOpenSourceEmbed, "#eALwmc5jf1P1");
        player.set("iterations", 1);
      }, false);

      // Observe "About OpenSource" to start animation when visible"
      const aboutOpenSourceIntersectionObserver = new IntersectionObserver(() => {
        playOnVisible(aboutOpenSourceEmbed, "#eALwmc5jf1P1");
      }, optionWholeElementIsVisible);

      aboutOpenSourceIntersectionObserver.observe(aboutOpenSourceEmbed);
    }

    // "About CCSolutions"
    const aboutCCSolutionsEmbed = document.querySelector("#about-ccsolutions");

    // Stop "About Vision" animation when loaded
    if (aboutCCSolutionsEmbed) {
      aboutCCSolutionsEmbed.addEventListener("load", () => {
        const player = this.animationPlayer(aboutCCSolutionsEmbed, "#eXu29g7HVya1");
        player.set("iterations", 3);
      }, false);

      // Observe "About CCSolutions" to start animation when visible"
      const aboutCCSolutionsIntersectionObserver = new IntersectionObserver(() => {
        playOnVisible(aboutCCSolutionsEmbed, "#eXu29g7HVya1", 3);
      }, optionWholeElementIsVisible);

      aboutCCSolutionsIntersectionObserver.observe(aboutCCSolutionsEmbed);
    }

    // "About Digitalization"
    const aboutDigitalizationEmbed = document.querySelector("#about-digitalization");

    // Stop "About Digitalization" animation when loaded
    if (aboutDigitalizationEmbed) {
      aboutDigitalizationEmbed.addEventListener("load", () => {
        const player = this.animationPlayer(aboutDigitalizationEmbed, "#eoK81BTCYEp1");
        player.set("iterations", 3);
      }, false);

      // Observe "About Digitalization" to start animation when visible"
      const aboutDigitalizationIntersectionObserver = new IntersectionObserver(() => {
        playOnVisible(aboutDigitalizationEmbed, "#eoK81BTCYEp1", 3);
      }, optionWholeElementIsVisible);

      aboutDigitalizationIntersectionObserver.observe(aboutDigitalizationEmbed);
    }

    // "About Team"
    const aboutTeamEmbed = document.querySelector("#about-team");

    // Stop "About Team" animation when loaded
    if (aboutTeamEmbed) {
      aboutTeamEmbed.addEventListener("load", () => {
        const player = this.animationPlayer(aboutTeamEmbed, "#eLQVzFGSlIT1");
        player.set("iterations", 3);
      }, false);

      // Observe "About Team" to start animation when visible"
      const aboutTeamIntersectionObserver = new IntersectionObserver(() => {
        playOnVisible(aboutTeamEmbed, "#eLQVzFGSlIT1", 3);
      }, optionWholeElementIsVisible);

      aboutTeamIntersectionObserver.observe(aboutTeamEmbed);
    }

    // "Ani Antony"
    const aniANtonyEmbed = document.querySelector("#ani-antony");

    // Stop "Ani Antony" animation when loaded
    if (aniANtonyEmbed) {
      aniANtonyEmbed.addEventListener("load", () => {
        const player = this.animationPlayer(aniANtonyEmbed, "#eMWQSLcNFm81");
        player.set("iterations", 1);
      }, false);

      // Observe "Ani Antony" to start animation when visible"
      const aniANtonyIntersectionObserver = new IntersectionObserver(() => {
        playOnVisible(aniANtonyEmbed, "#eMWQSLcNFm81");
      }, optionWholeElementIsVisible);

      aniANtonyIntersectionObserver.observe(aniANtonyEmbed);
    }

    // "Services Robotic Arm"
    const servicesRoboticArmEmbed = document.querySelector("#services-robotic-arm");

    // Stop "Services Robotic Arm" animation when loaded
    if (servicesRoboticArmEmbed) {
      servicesRoboticArmEmbed.addEventListener("load", () => {
        const player = this.animationPlayer(servicesRoboticArmEmbed, "#e8CdnGNchjk1");
        player.set("iterations", 1);
      }, false);

      // Observe "Services Robotic Arm" to start animation when visible"
      const servicesRoboticArmIntersectionObserver = new IntersectionObserver(() => {
        playOnVisible(servicesRoboticArmEmbed, "#e8CdnGNchjk1");
      }, optionWholeElementIsVisible);

      servicesRoboticArmIntersectionObserver.observe(servicesRoboticArmEmbed);
    }

    // "Blog She Robot"
    const blogSheRobotEmbed = document.querySelector("#blog-she-robot");

    // Stop "Blog She Robot" animation when loaded
    if (blogSheRobotEmbed) {
      blogSheRobotEmbed.addEventListener("load", () => {
        const player = this.animationPlayer(blogSheRobotEmbed, "#esZ7BXjxyfD1");
        player.set("iterations", 1);
      }, false);

      // Observe "Blog She Robot" to start animation when visible"
      const blogSheRobotIntersectionObserver = new IntersectionObserver(() => {
        playOnVisible(blogSheRobotEmbed, "#esZ7BXjxyfD1");
      }, optionWholeElementIsVisible);

      blogSheRobotIntersectionObserver.observe(blogSheRobotEmbed);
    }

    // "Blog He Robot"
    const blogHeRobotEmbed = document.querySelector("#blog-he-robot");

    // Stop "Blog He Robot" animation when loaded
    if (blogHeRobotEmbed) {
      blogHeRobotEmbed.addEventListener("load", () => {
        const player = this.animationPlayer(blogHeRobotEmbed, "#ec8E9klW0wC1");
        player.set("iterations", 1);
      }, false);

      // Observe "Blog He Robot" to start animation when visible"
      const blogHeRobotIntersectionObserver = new IntersectionObserver(() => {
        playOnVisible(blogHeRobotEmbed, "#ec8E9klW0wC1");
      }, optionWholeElementIsVisible);

      blogHeRobotIntersectionObserver.observe(blogHeRobotEmbed);
    }
  };

  playAnimation(event) {
    const animationEmbed = document.querySelector(event.params.embed);
    const player = this.animationPlayer(animationEmbed, event.params.svg);
    player
      .set("iterations", event.params.iterations)
      .restart();
  };

  pauseAnimation(event) {
    const animationEmbed = document.querySelector(event.params.embed);
    const player = this.animationPlayer(animationEmbed, event.params.svg);
    player.seek(event.params.offset).pause();
  };

  animationPlayer(embed, svgID) {
    const svgDoc = embed?.contentDocument;
    const svgAnimation = svgDoc?.querySelector(svgID);
    return svgAnimation?.svgatorPlayer;
  }

}
