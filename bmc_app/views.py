import pandas as pd
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class CandidateExcelDataView(APIView):
    def get(self, request):
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            csv_path = os.path.join(base_dir, "data", "bmc_candidates.csv")

            if not os.path.exists(csv_path):
                return Response(
                    {"error": f"CSV file not found at {csv_path}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            # Load CSV and clean it
            df = pd.read_csv(csv_path)
            df = df.fillna("")
            df["Ward_No"] = df["Ward_No"].astype(str).str.strip()
            df["Ward_Name"] = df["Ward_Name"].astype(str).str.strip()
            df["Votes"] = pd.to_numeric(df["Votes"], errors="coerce").fillna(0)

            # Remove duplicates
            df = df.drop_duplicates(subset=["Ward_No", "Candidate_Name", "Votes"], keep="first")

            # Find winners
            winners = df.loc[df.groupby("Ward_No")["Votes"].idxmax()].reset_index(drop=True)
            winners = winners.drop_duplicates(subset=["Ward_No"])

            data = []

            for _, winner in winners.iterrows():
                ward_no = winner["Ward_No"]
                ward_candidates = (
                    df[df["Ward_No"] == ward_no]
                    .sort_values(by="Votes", ascending=False)
                    .reset_index(drop=True)
                )

                # Get votes for margin calculation
                winner_votes = ward_candidates.iloc[0]["Votes"] if len(ward_candidates) > 0 else 0
                runnerup_votes = ward_candidates.iloc[1]["Votes"] if len(ward_candidates) > 1 else 0
                total_votes = ward_candidates["Votes"].sum()

                vote_margin = int(winner_votes - runnerup_votes)
                margin_percent = round((vote_margin / total_votes * 100), 2) if total_votes > 0 else 0

                data.append({
                    "Ward_No": ward_no,
                    "Ward_Name": winner["Ward_Name"],
                    "Winner": {
                        "Candidate_Name": winner["Candidate_Name"],
                        "Party_Name": winner["Party_Name"],
                        "Votes": int(winner_votes),
                        "Vote_Share_Percentage": winner.get("Vote_Share_Percentage", ""),
                        "Position": int(winner.get("Position", 1)),
                        "Margin": vote_margin,
                        "Margin_Percentage": margin_percent,
                    },
                    "Candidates": ward_candidates.to_dict(orient="records"),
                })

            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
