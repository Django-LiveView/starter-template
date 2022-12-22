import {connect, startEvents} from './webSocketsCli.js';
import { Application } from "./vendors/stimulus.js";
import pageController from "./controllers/page_controller.js";
import catsController from "./controllers/cats_controller.js";
import loginController from "./controllers/login_controller.js";
import profileController from "./controllers/profile_controller.js";

/*
   INITIALIZATION
 */

// WebSocket connection
connect();
startEvents();

// Stimulus
window.Stimulus = Application.start();

// Register all controllers
Stimulus.register("page", pageController);
Stimulus.register("cats", catsController);
Stimulus.register("login", loginController);
Stimulus.register("profile", profileController);
