// Official page access was blocked. These are explicitly provisional study rules.
export const QUALIFICATION = {
  name: "소방설비기사(기계)",
  subjects: ["소방원론", "소방유체역학", "소방관계법규", "소방기계시설의 구조 및 원리"] as const,
  exam: { questionCount: 80, perSubject: 20, durationMinutes: 120, choiceCount: 4, passScore: 60, subjectCutoff: 40 },
  rulesVerificationStatus: "pending",
  officialSource: "https://www.q-net.or.kr/crf005.do?id=crf00503&jmCd=1900",
  bankId: "main", storageNamespace: "fire-mechanical-cbt:v1",
} as const;
