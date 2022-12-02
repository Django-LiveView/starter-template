import { Controller } from "../vendors/stimulus.js";
import { parallax } from "../mixins/miscellaneous.js";

export default class extends Controller {

  connect() {
    // home page parallax effect
    const headerBgX = 0.1;
    const headerBgY = 0.2;
    const valuesBgX = 0.15;
    const valuesBgY = -0.1;
    const devTypesBgX = 0.1;
    const devTypesBgY = 0.1;
    const technologyBgX = -0.17;
    const technologyBgY = 0.09;
    const blogBgX = 0.2;
    const blogBgY = 0.13;

    const headerBg = document.querySelector("#header-bg");
    const valuesBg = document.querySelector("#values-bg");
    const devTypesBg = document.querySelector("#dev-types-bg");
    const technologyBg = document.querySelector("#technology-bg");
    const blogBg = document.querySelector("#blog-bg");

    parallax(headerBg, headerBgX, headerBgY);
    parallax(valuesBg, valuesBgX, valuesBgY);
    parallax(devTypesBg, devTypesBgX, devTypesBgY);
    parallax(technologyBg, technologyBgX, technologyBgY);
    parallax(blogBg, blogBgX, blogBgY);

    // about us page parallax effect
    const aboutHeaderBgX = -0.1;
    const aboutHeaderBgY = 0.2;
    const aboutWhyUsBgX = -0.1;
    const aboutWhyUsBgY = -0.2;
    const aboutGrowthBgX = 0.2;
    const aboutGrowthBgY = 0.2;
    const aboutPartnerBgX = 0.1;
    const aboutPartnerBgY = -0.05;

    const aboutHeaderBg = document.querySelector("#about-header-bg");
    const aboutWhyUsBg = document.querySelector("#about-why-us-bg");
    const aboutGrowthBg = document.querySelector("#about-growth-bg");
    const aboutPartnerBg = document.querySelector("#about-partner-bg");

    parallax(aboutHeaderBg, aboutHeaderBgX, aboutHeaderBgY);
    parallax(aboutWhyUsBg, aboutWhyUsBgX, aboutWhyUsBgY);
    parallax(aboutGrowthBg, aboutGrowthBgX, aboutGrowthBgY);
    parallax(aboutPartnerBg, aboutPartnerBgX, aboutPartnerBgY);

    // services page parallax effect
    const servicesHeaderBgX = 0.1;
    const servicesHeaderBgY = 0.2;
    const servicesWebsitesBgX = -0.2;
    const servicesWebsitesBgY = -0.15;

    const servicesHeaderBg = document.querySelector("#services-header-bg");
    const servicesWebsitesBg = document.querySelector("#services-websites-bg");

    parallax(servicesHeaderBg, servicesHeaderBgX, servicesHeaderBgY);
    parallax(servicesWebsitesBg, servicesWebsitesBgX, servicesWebsitesBgY);

    // blog page parallax effect
    const blogHeaderBgX = 0.3;
    const blogHeaderBgY = 0.05;
    const blogPostHeaderBgX = 0.3;
    const blogPostHeaderBgY = 0.05;
    const blogPostBodyBgX = 0.1;
    const blogPostBodyBgY = 0.35;

    const blogHeaderBg = document.querySelector("#blog-header-bg");
    const blogPostHeaderBg = document.querySelector("#blog-post-header-bg");
    const blogPostBodyBg = document.querySelector("#blog-post-body-bg");

    parallax(blogHeaderBg, blogHeaderBgX, blogHeaderBgY);
    parallax(blogPostHeaderBg, blogPostHeaderBgX, blogPostHeaderBgY);
    parallax(blogPostBodyBg, blogPostBodyBgX, blogPostBodyBgY);

    // projects page parallax effect
    const projectsMainHeaderBgX = 0.2;
    const projectsMainHeaderBgY = 0.2;

    const projectsMainHeaderBg = document.querySelector("#projects-main-header-bg");

    parallax(projectsMainHeaderBg, projectsMainHeaderBgX, projectsMainHeaderBgY);

    // project single page parallax effect
    const projectSingleHeaderBgX = 0.1;
    const projectSingleHeaderBgY = 0.25;

    const projectSingleHeaderBg = document.querySelector("#project-header-bg");

    parallax(projectSingleHeaderBg, projectSingleHeaderBgX, projectSingleHeaderBgY);

    // legal page parallax effect
    const legalHeaderBgX = 0.1;
    const legalHeaderBgY = 0.3;

    const legalHeaderBg = document.querySelector("#legal-header-bg");

    parallax(legalHeaderBg, legalHeaderBgX, legalHeaderBgY);

    // onscroll event listner
    window.onscroll = () => {
      // home page parallax effect
      parallax(headerBg, headerBgX, headerBgY);
      parallax(valuesBg, valuesBgX, valuesBgY);
      parallax(devTypesBg, devTypesBgX, devTypesBgY);
      parallax(technologyBg, technologyBgX, technologyBgY);
      parallax(blogBg, blogBgX, blogBgY);

      // about us page parallax effect
      parallax(aboutHeaderBg, aboutHeaderBgX, aboutHeaderBgY);
      parallax(aboutWhyUsBg, aboutWhyUsBgX, aboutWhyUsBgY);
      parallax(aboutGrowthBg, aboutGrowthBgX, aboutGrowthBgY);
      parallax(aboutPartnerBg, aboutPartnerBgX, aboutPartnerBgY);

      // services page parallax effect
      parallax(servicesHeaderBg, servicesHeaderBgX, servicesHeaderBgY);
      parallax(servicesWebsitesBg, servicesWebsitesBgX, servicesWebsitesBgY);

      // blog page parallax effect
      parallax(blogHeaderBg, blogHeaderBgX, blogHeaderBgY);
      parallax(blogPostHeaderBg, blogPostHeaderBgX, blogPostHeaderBgY);
      parallax(blogPostBodyBg, blogPostBodyBgX, blogPostBodyBgY);

      // projects page parallax effect
      parallax(projectsMainHeaderBg, projectsMainHeaderBgX, projectsMainHeaderBgY);

      // project single page parallax effect
      parallax(projectSingleHeaderBg, projectSingleHeaderBgX, projectSingleHeaderBgY);

      // legal page parallax effect
      parallax(legalHeaderBg, legalHeaderBgX, legalHeaderBgY);
    };
  };
}
