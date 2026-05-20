package main

import (
	"encoding/csv"
	"fmt"
	"log"
	"os"
	"strconv"
)

var requiredColumns = []string{
	"participant", "site_id", "condition", "trial", "actor_role",
	"observer_role", "behavior_valence", "dispositional_attribution",
	"situational_attribution", "perceived_constraint", "actual_constraint",
	"choice_freedom", "correspondence_inference", "cognitive_load",
	"perspective_taking", "accountability_pressure", "evidence_strength",
	"empathy", "moral_blame", "punishment_recommendation",
	"cultural_individualism", "structural_awareness", "response_time_ms",
}

func main() {
	if len(os.Args) < 2 {
		log.Fatal("Usage: go run go/validator.go data/fundamental_attribution_error_trials.csv")
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

	conditionCounts := map[string]int{}
	errors := 0

	for rowNum, row := range rows[1:] {
		line := rowNum + 2
		conditionCounts[row[index["condition"]]]++

		checkRange(row, index, "trial", 1, 1000000, line, &errors)
		checkRange(row, index, "dispositional_attribution", 0, 10, line, &errors)
		checkRange(row, index, "situational_attribution", 0, 10, line, &errors)
		checkRange(row, index, "perceived_constraint", 0, 10, line, &errors)
		checkRange(row, index, "actual_constraint", 0, 10, line, &errors)
		checkRange(row, index, "choice_freedom", 0, 10, line, &errors)
		checkRange(row, index, "correspondence_inference", 0, 10, line, &errors)
		checkRange(row, index, "cognitive_load", 0, 10, line, &errors)
		checkRange(row, index, "perspective_taking", 0, 10, line, &errors)
		checkRange(row, index, "accountability_pressure", 0, 10, line, &errors)
		checkRange(row, index, "evidence_strength", 0, 10, line, &errors)
		checkRange(row, index, "empathy", 0, 10, line, &errors)
		checkRange(row, index, "moral_blame", 0, 10, line, &errors)
		checkRange(row, index, "punishment_recommendation", 0, 10, line, &errors)
		checkRange(row, index, "cultural_individualism", 0, 10, line, &errors)
		checkRange(row, index, "structural_awareness", 0, 10, line, &errors)
		checkRange(row, index, "response_time_ms", 150, 1000000, line, &errors)
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
