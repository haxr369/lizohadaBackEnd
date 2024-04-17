import { blogScraper } from "./common/blogScraper.js";
import { blogDetailScraper } from "./common/blogDetailScraper.mjs";
import {
  requestBathWrite,
  requestRecentPostdate,
} from "./common/ddbRequest.mjs";
/**
 * event = {
 *  keyword : "울릉 여행",
 *  count : "30"
 * }
 *
 */

export const handler = async (event, context) => {
  const body = event;

  try {
    // inputData = JSON.parse(body);
    console.log("[User Input]: ", body);
  } catch (error) {
    console.error("[JSON Parsing Error]:", error);
    return { statusCode: 400, body: "Invalid JSON format" };
  }

  if (!body.hasOwnProperty("keyword")) {
    console.error("[Invalid Request]: No content provided");
    return { statusCode: 400, body: "No content provided" };
  }

  const recentPostDate = await requestRecentPostdate(body.keyword);

  let blogs = await blogScraper(body.keyword, body.count, recentPostDate);
  // map은 함수 콜을 하고 그 결과를 기다리고 다음 콜한다. 100개 스크랩에 -> 37초
  // 매우 느린 방법이지만, 하나씩 하기에 막히진 않는다.
  let putRequests = [];
  for (const b of blogs) {
    console.log(b.link);
    const item = await blogDetailScraper(b);
    putRequests.push({
      PutRequest: {
        Item: item,
      },
    });
    await delay(1000);
  }
  requestBathWrite(putRequests);
  // const filePath = `./results/${body.keyword}.json`;
  // fs.writeFileSync(filePath, JSON.stringify(result, null, 2), "utf-8");
  return {
    statusCode: 200,
    body: JSON.stringify(body.keyword + " 스크랩핑 끝"),
  };
};

function delay(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
