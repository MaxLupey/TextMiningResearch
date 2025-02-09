import {UserData} from "../../interfaces/auth.context.interface"
import { tminginRequest } from "../requests/tminingRequests";


export const fetchUserData = async (): Promise<UserData> => {
        const response = await tminginRequest.profileInfo();
        const data = response.data;
        if (response.status === 401) {
            throw new Error("Not authorized");
        }
        if (response.status !== 200) {
            throw new Error(data.message);
        }
        return {
            firstName: data[0],
            lastName: data[1],
            avatarUrl: data[2],
        };
};