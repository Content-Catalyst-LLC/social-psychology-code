package main

import (
	"encoding/csv"
	"fmt"
	"log"
	"os"
	"strconv"
)

var requiredColumns = []string{
	"participant", "session_id", "group_id", "scenario_id", "site_id",
	"institution_context", "judgment_domain", "heuristic_type", "condition", "trial",
	"anchor_value", "true_value", "estimate", "base_rate",
	"individuating_information_strength", "representativeness_rating",
	"availability_salience", "affect_valence", "perceived_risk", "perceived_benefit",
	"frame_type", "choice_binary", "confidence_rating", "actual_accuracy",
	"confirmation_tendency", "disconfirming_evidence_exposure", "overconfidence_score",
	"response_time_ms", "debiasing_intervention_strength", "institutional_accountability",
	"feedback_quality", "decision_quality",
}

func main() {
	if len(os.Args) < 2 {
		log.Fatal("Usage: go run go/validator.go data/heuristics_biases_trials.csv")
	}

	path := os.Args[1]
	file, err := os.Open(path)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	reader := csv.NewReader(file)
	reader.FieldsPerRecord = -1
	rows, err := reader.ReadAll()
	if err != nil {
		log.Fatal(err)
	}
	if len(rows) < 2 {
		log.Fatal("CSV must contain a header and at least one data row")
	}

	header := rows[0]
	index := map[string]int{}
	for i, col := range header {
		index[col] = i
	}

	missing := []string{}
	for _, col := range requiredColumns {
		if _, ok := index[col]; !ok {
			missing = append(missing, col)
		}
	}
	if len(missing) > 0 {
		log.Fatalf("Missing required columns: %v", missing)
	}

	errors := 0
	heuristicCounts := map[string]int{}

	for rowNum, row := range rows[1:] {
		line := rowNum + 2
		heuristicCounts[row[index["heuristic_type"]]]++

		checkRange(row, index, "trial", 1, 1000000, line, &errors)
		checkRange(row, index, "anchor_value", -1000, 1000, line, &errors)
		checkRange(row, index, "true_value", -1000, 1000, line, &errors)
		checkRange(row, index, "estimate", -1000, 1000, line, &errors)
		checkRange(row, index, "base_rate", 0, 1, line, &errors)
		checkRange(row, index, "affect_valence", -10, 10, line, &errors)
		checkRange(row, index, "choice_binary", 0, 1, line, &errors)
		checkRange(row, index, "overconfidence_score", -100, 100, line, &errors)
		checkRange(row, index, "response_time_ms", 150, 10000000, line, &errors)

		for _, col := range []string{
			"individuating_information_strength", "representativeness_rating",
			"availability_salience", "confirmation_tendency", "disconfirming_evidence_exposure",
			"debiasing_intervention_strength", "institutional_accountability", "feedback_quality",
		} {
			checkRange(row, index, col, 0, 10, line, &errors)
		}

		for _, col := range []string{
			"perceived_risk", "perceived_benefit", "confidence_rating", "actual_accuracy", "decision_quality",
		} {
			checkRange(row, index, col, 0, 100, line, &errors)
		}
	}

	fmt.Printf("Validated file: %s\n", path)
	fmt.Printf("Rows checked: %d\n", len(rows)-1)
	fmt.Printf("Validation errors: %d\n", errors)
	fmt.Println("Heuristic counts:")
	for heuristic, count := range heuristicCounts {
		fmt.Printf("  %s: %d\n", heuristic, count)
	}

	if errors > 0 {
		os.Exit(2)
	}
}

func checkRange(row []string, index map[string]int, col string, min float64, max float64, line int, errors *int) {
	value, err := strconv.ParseFloat(row[index[col]], 64)
	if err != nil {
		fmt.Printf("Line %d: %s is not numeric: %s\n", line, col, row[index[col]])
		*errors = *errors + 1
		return
	}
	if value < min || value > max {
		fmt.Printf("Line %d: %s out of range [%.1f, %.1f]: %.3f\n", line, col, min, max, value)
		*errors = *errors + 1
	}
}
