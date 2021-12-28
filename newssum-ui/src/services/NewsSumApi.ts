import NewsSource from "../models/NewsSource";
import Logger from "./Logger";

export default class NewsSumApi {
  static async getSources(): Promise<NewsSource[]> {
    try {
      // TODO use relative url
      var response = await fetch("https://news-sum.appspot.com/list", {
        "method": "GET"
      });
      if (response.ok) {
        return JSON.parse(await response.text());
      } else {
        Logger.log("Failed to fetch news sources " + response.status + ": " + response.statusText);
      }
    } catch (err: unknown) {
      Logger.log("Failed to fetch news sources: ");
      if (typeof err === "string") {
        Logger.log(err);
      } else if (err instanceof Error) {
        Logger.log(err.message);
      }

    }
    return Promise.reject("Failed to retrieve news sources");
  }
}
