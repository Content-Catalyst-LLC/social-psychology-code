package main

import (
	"encoding/csv"
	"fmt"
	"log"
	"os"
	"strconv"
)

var requiredColumns = []string{
	"participant", "site_id", "condition", "wave", "target_group", "group_status",
	"contact_frequency", "contact_quality", "equal_status", "common_goals",
	"cooperation", "institutional_support", "voluntariness", "negative_contact",
	"indirect_contact", "intergroup_anxiety", "empathy", "perspective_taking",
	"trust", "perceived_threat", "prejudice_pre", "prejudice_post",
	"stereotype_endorsement", "future_contact_willingness", "social_distance",
	"inclusive_norm_perception", "response_time_ms",
}

func main() {
	if len(os.Args) < 2 {
		log.Fatal("Usage: go run go/validator.go data/contact_hypothesis_trials.csv")
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
	statusCounts := map[string]int{}
	errors := 0

	for rowNum, row := range rows[1:] {
		line := rowNum + 2
		conditionCounts[row[index["condition"]]]++
		statusCounts[row[index["group_status"]]]++

		checkRange(row, index, "wave", 1, 1000000, line, &errors)
		checkRange(row, index, "contact_frequency", 0, 10, line, &errors)
		checkRange(row, index, "contact_quality", 0, 10, line, &errors)
		checkRange(row, index, "equal_status", 0, 10, line, &errors)
		checkRange(row, index, "common_goals", 0, 10, line, &errors)
		checkRange(row, index, "cooperation", 0, 10, line, &errors)
		checkRange(row, index, "institutional_support", 0, 10, line, &errors)
		checkRange(row, index, "voluntariness", 0, 10, line, &errors)
		checkRange(row, index, "negative_contact", 0, 10, line, &errors)
		checkRange(row, index, "indirect_contact", 0, 10, line, &errors)
		checkRange(row, index, "intergroup_anxiety", 0, 10, line, &errors)
		checkRange(row, index, "empathy", 0, 10, line, &errors)
		checkRange(row, index, "perspective_taking", 0, 10, line, &errors)
		checkRange(row, index, "trust", 0, 10, line, &errors)
		checkRange(row, index, "perceived_threat", 0, 10, line, &errors)
		checkRange(row, index, "prejudice_pre", 0, 10, line, &errors)
		checkRange(row, index, "prejudice_post", 0, 10, line, &errors)
		checkRange(row, index, "stereotype_endorsement", 0, 10, line, &errors)
		checkRange(row, index, "future_contact_willingness", 0, 10, line, &errors)
		checkRange(row, index, "social_distance", 0, 10, line, &errors)
		checkRange(row, index, "inclusive_norm_perception", 0, 10, line, &errors)
		checkRange(row, index, "response_time_ms", 150, 1000000, line, &errors)
	}

	fmt.Printf("Validated file: %s\n", path)
	fmt.Printf("Rows checked: %d\n", len(rows)-1)
	fmt.Printf("Validation errors: %d\n", errors)
	fmt.Println("Condition counts:")
	for condition, count := range conditionCounts {
		fmt.Printf("  %s: %d\n", condition, count)
	}
	fmt.Println("Group status counts:")
	for status, count := range statusCounts {
		fmt.Printf("  %s: %d\n", status, count)
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
