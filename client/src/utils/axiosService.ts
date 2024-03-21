import axios from "axios";

import {urls, tminingUrl} from "../api/routers/tminingRouters";

export const axiosService = axios.create({baseURL: tminingUrl})