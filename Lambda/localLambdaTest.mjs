import { handler } from "./index.mjs";

const regionNames = [
  "강릉",
  "동해",
  "삼척",
  "속초",
  "원주",
  // "춘천",
  // "태백",
  // "고성",
  "양구",
  "양양",
  "영월",
  "인제",
  "정선",
  "철원",
  "평창",
  "홍천",
  "화천",
  "횡성",
  "청주",
  "상당",
  // "서원",
  // "흥덕",
  // "청원",
  // "충주",
  // "제천",
  // "보은",
  // "옥천",
  // "영동",
  // "진천",
  // "음성",
  // "괴산",
  // "단양",
  // "증평",
];
const context = {};
// 정규표현식을 사용하여 ""을 제외한 지역명 추출
// JSON 형태로 변환
const result = regionNames.map((name) => ({
  keyword: `${name} 여행`,
  count: "17",
}));
// let cnt = 0;
async function go() {
  for (const event of result) {
    await handler(event, context)
      .then((result) => console.log(result))
      .catch((error) => console.error(error));
    await delay(10000);
    // cnt++;
    // if (cnt > 3) {
    //   break;
    // }
  }
}
go();
function delay(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
