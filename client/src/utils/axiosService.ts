import axios from "axios";

import {tminingUrl} from "../api/routers/tminingRouters";

export const axiosService = axios.create({baseURL: tminingUrl})