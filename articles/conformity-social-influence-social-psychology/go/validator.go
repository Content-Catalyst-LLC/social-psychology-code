package main

import (
	"encoding/csv"
	"fmt"
	"log"
	"os"
	"strconv"
)

var requiredColumns = []string{
	"participant", "session_id", "group_id", "scenario_id", "site_id", "context",
	"condition", "trial", "ambiguity", "majority_size", "unanimity", "visible_dissent",
	"cohesion", "normative_pressure", "informational_uncertainty", "status_strength",
	"public_response", "private_response", "group_identification", "social_identity_salience",
	"minority_consistency", "network_exposure", "social_proof_metrics", "algorithmic_amplification",
	"conformed", "dissented", "confidence_pre", "confidence_post", "response_time_ms",
}

func main() {
	if len(os.Args) < 2 {
		log.Fatal("Usage: go run go/validator.go data/conformity_trials.csv")
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
	conditionCounts := map[string]int{}

	for rowNum, row := range rows[1:] {
		line := rowNum + 2
		conditionCounts[row[index["condition"]]]++

		checkRange(row, index, "trial", 1, 1000000, line, &errors)
		checkRange(row, index, "majority_size", 0, 1000000, line, &errors)
		checkRange(row, index, "response_time_ms", 150, 10000000, line, &errors)

		for _, col := range []string{"public_response", "private_response", "conformed", "dissented"} {
			checkRange(row, index, col, 0, 1, line, &errors)
		}

		for _, col := range []string{
			"ambiguity", "unanimity", "visible_dissent", "cohesion",
			"normative_pressure", "informational_uncertainty", "status_strength",
			"group_identification", "social_identity_salience", "minority_consistency",
			"network_exposure", "social_proof_metrics", "algorithmic_amplification",
		} {
			checkRange(row, index, col, 0, 10, line, &errors)
		}

		for _, col := range []string{"confidence_pre", "confidence_post"} {
			checkRange(row, index, col, 0, 100, line, &errors)
		}
	}

	fmt.Printf("Validated file: %s\n", path)
	fmt.Printf("Rows checked: %d\n", len(rows)-1)
	fmt.Printf("Validation errors: %d\n", errors)
	fmt.Println("Condition counts:")
	for condition, count := range conditionCounts {
		fmt.Printf("  %s: %d\n", condition, count)
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
