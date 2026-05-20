package main

import (
	"encoding/csv"
	"fmt"
	"log"
	"os"
	"strconv"
)

var requiredColumns = []string{
	"participant", "site_id", "condition", "trial", "outcome_valence",
	"actor_target", "self_other", "internal_attribution", "external_attribution",
	"stable_attribution", "controllable_attribution", "responsibility_rating",
	"blame_rating", "credit_claiming", "excuse_making", "self_esteem",
	"ego_threat", "task_importance", "outcome_expectancy", "perceived_fairness",
	"evidence_strength", "learning_intention", "accountability_pressure",
	"response_time_ms",
}

func main() {
	if len(os.Args) < 2 {
		log.Fatal("Usage: go run go/validator.go data/self_serving_bias_trials.csv")
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
	valenceCounts := map[string]int{}
	errors := 0

	for rowNum, row := range rows[1:] {
		line := rowNum + 2
		conditionCounts[row[index["condition"]]]++
		valenceCounts[row[index["outcome_valence"]]]++

		checkRange(row, index, "trial", 1, 1000000, line, &errors)
		checkRange(row, index, "internal_attribution", 0, 10, line, &errors)
		checkRange(row, index, "external_attribution", 0, 10, line, &errors)
		checkRange(row, index, "stable_attribution", 0, 10, line, &errors)
		checkRange(row, index, "controllable_attribution", 0, 10, line, &errors)
		checkRange(row, index, "responsibility_rating", 0, 10, line, &errors)
		checkRange(row, index, "blame_rating", 0, 10, line, &errors)
		checkRange(row, index, "credit_claiming", 0, 10, line, &errors)
		checkRange(row, index, "excuse_making", 0, 10, line, &errors)
		checkRange(row, index, "self_esteem", 0, 10, line, &errors)
		checkRange(row, index, "ego_threat", 0, 10, line, &errors)
		checkRange(row, index, "task_importance", 0, 10, line, &errors)
		checkRange(row, index, "outcome_expectancy", 0, 10, line, &errors)
		checkRange(row, index, "perceived_fairness", 0, 10, line, &errors)
		checkRange(row, index, "evidence_strength", 0, 10, line, &errors)
		checkRange(row, index, "learning_intention", 0, 10, line, &errors)
		checkRange(row, index, "accountability_pressure", 0, 10, line, &errors)
		checkRange(row, index, "response_time_ms", 150, 1000000, line, &errors)
	}

	fmt.Printf("Validated file: %s\n", path)
	fmt.Printf("Rows checked: %d\n", len(rows)-1)
	fmt.Printf("Validation errors: %d\n", errors)
	fmt.Println("Condition counts:")
	for condition, count := range conditionCounts {
		fmt.Printf("  %s: %d\n", condition, count)
	}
	fmt.Println("Outcome valence counts:")
	for valence, count := range valenceCounts {
		fmt.Printf("  %s: %d\n", valence, count)
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
