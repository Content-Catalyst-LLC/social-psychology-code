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
	"condition", "trial", "target_group", "evaluator_group", "stereotype_strength",
	"warmth_rating", "competence_rating", "prejudice_rating", "perceived_threat",
	"perceived_competition", "perceived_status", "social_distance", "contact_quality",
	"contact_quantity", "institutional_support", "stereotype_threat_salience",
	"identity_safety", "implicit_score", "explicit_attitude", "discrimination_tendency",
	"behavioral_outcome", "performance_score", "response_time_ms", "structured_criteria", "accountability",
}

func main() {
	if len(os.Args) < 2 {
		log.Fatal("Usage: go run go/validator.go data/stereotypes_prejudice_trials.csv")
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
		checkRange(row, index, "response_time_ms", 250, 10000000, line, &errors)
		checkRange(row, index, "implicit_score", -3, 3, line, &errors)
		checkRange(row, index, "explicit_attitude", -100, 100, line, &errors)

		for _, col := range []string{
			"stereotype_strength", "warmth_rating", "competence_rating", "prejudice_rating",
			"perceived_threat", "perceived_competition", "perceived_status", "social_distance",
			"contact_quality", "contact_quantity", "institutional_support", "stereotype_threat_salience",
			"identity_safety", "structured_criteria", "accountability",
		} {
			checkRange(row, index, col, 0, 10, line, &errors)
		}

		for _, col := range []string{"discrimination_tendency", "behavioral_outcome", "performance_score"} {
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
