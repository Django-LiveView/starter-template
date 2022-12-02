import { manageHistory } from "./manage_history.js";
import {connect, startEvents} from './webSocketsCli.js';
import { Application } from "./vendors/stimulus.js";
import headerController from "./controllers/header_controller.js";
import pageController from "./controllers/page_controller.js";
import teamController from "./controllers/about_us/team_controller.js";
import growthController from "./controllers/about_us/growth_controller.js";
import contactController from "./controllers/contact_controller.js";
import blogController from "./controllers/blog_controller.js";
import parallaxController from "./controllers/parallax_controller.js";
import projectController from "./controllers/project_controller.js";
import servicesController from "./controllers/services_controller.js";
import animationsController from "./controllers/animations_controller.js";

/*
   INITIALIZATION
 */
manageHistory();

// WebSocket connection
connect();
startEvents();

// Stimulus
window.Stimulus = Application.start();
// Register all controllers
Stimulus.register("header", headerController);
Stimulus.register("page", pageController);
Stimulus.register("team", teamController);
Stimulus.register("growth", growthController);
Stimulus.register("contact", contactController);
Stimulus.register("blog", blogController);
Stimulus.register("parallax", parallaxController);
Stimulus.register("project", projectController);
Stimulus.register("services", servicesController);
Stimulus.register("animations", animationsController);
