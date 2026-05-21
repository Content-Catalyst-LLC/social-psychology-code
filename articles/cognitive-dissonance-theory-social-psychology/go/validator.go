package main

import (
	"encoding/csv"
	"fmt"
	"log"
	"os"
	"strconv"
)

var requiredColumns = []string{
	"participant", "session_id", "group_id", "scenario_id", "site_id", "institution_context",
	"paradigm", "condition", "trial", "pre_attitude", "post_attitude",
	"counter_attitudinal_behavior", "perceived_choice", "perceived_responsibility",
	"identity_threat", "self_affirmation", "external_justification", "public_commitment",
	"effort_cost", "outcome_value", "chosen_pre_value", "chosen_post_value",
	"rejected_pre_value", "rejected_post_value", "belief_disconfirmation_strength",
	"commitment_strength", "proselytizing_intensity", "coherence_pressure",
	"dissonance_discomfort", "response_time_ms", "institutional_identity_threat",
	"sunk_cost", "evidence_strength", "accountability", "policy_reversal_willingness",
}

func main() {
	if len(os.Args) < 2 {
		log.Fatal("Usage: go run go/validator.go data/dissonance_trials.csv")
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
	paradigmCounts := map[string]int{}

	for rowNum, row := range rows[1:] {
		line := rowNum + 2
		paradigmCounts[row[index["paradigm"]]]++

		checkRange(row, index, "trial", 1, 1000000, line, &errors)
		checkRange(row, index, "response_time_ms", 150, 10000000, line, &errors)

		for _, col := range []string{"pre_attitude", "post_attitude"} {
			checkRange(row, index, col, -100, 100, line, &errors)
		}

		for _, col := range []string{
			"counter_attitudinal_behavior", "perceived_choice", "perceived_responsibility",
			"identity_threat", "self_affirmation", "external_justification", "public_commitment",
			"effort_cost", "belief_disconfirmation_strength", "commitment_strength",
			"coherence_pressure", "dissonance_discomfort", "institutional_identity_threat",
			"sunk_cost", "evidence_strength", "accountability",
		} {
			checkRange(row, index, col, 0, 10, line, &errors)
		}

		for _, col := range []string{
			"outcome_value", "chosen_pre_value", "chosen_post_value", "rejected_pre_value",
			"rejected_post_value", "proselytizing_intensity", "policy_reversal_willingness",
		} {
			checkRange(row, index, col, 0, 100, line, &errors)
		}
	}

	fmt.Printf("Validated file: %s\n", path)
	fmt.Printf("Rows checked: %d\n", len(rows)-1)
	fmt.Printf("Validation errors: %d\n", errors)
	fmt.Println("Paradigm counts:")
	for paradigm, count := range paradigmCounts {
		fmt.Printf("  %s: %d\n", paradigm, count)
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
