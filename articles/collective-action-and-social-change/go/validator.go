package main

import (
	"encoding/csv"
	"fmt"
	"log"
	"os"
	"strconv"
)

var requiredColumns = []string{
	"participant", "group_id", "condition", "trial", "movement_domain",
	"identity_strength", "perceived_injustice", "moral_outrage",
	"collective_efficacy", "network_support", "mobilization_exposure",
	"participation_cost", "perceived_repression_risk", "free_rider_incentive",
	"participation_intention", "action_participation", "digital_engagement",
	"offline_engagement", "recruitment_source", "institutional_response",
	"perceived_legitimacy", "movement_outcome", "response_time_ms",
}

func main() {
	if len(os.Args) < 2 {
		log.Fatal("Usage: go run go/validator.go data/collective_action_trials.csv")
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
	domainCounts := map[string]int{}
	errors := 0

	for rowNum, row := range rows[1:] {
		line := rowNum + 2
		conditionCounts[row[index["condition"]]]++
		domainCounts[row[index["movement_domain"]]]++

		checkRange(row, index, "trial", 1, 1000000, line, &errors)
		checkRange(row, index, "identity_strength", 0, 10, line, &errors)
		checkRange(row, index, "perceived_injustice", 0, 10, line, &errors)
		checkRange(row, index, "moral_outrage", 0, 10, line, &errors)
		checkRange(row, index, "collective_efficacy", 0, 10, line, &errors)
		checkRange(row, index, "network_support", 0, 10, line, &errors)
		checkRange(row, index, "mobilization_exposure", 0, 10, line, &errors)
		checkRange(row, index, "participation_cost", 0, 10, line, &errors)
		checkRange(row, index, "perceived_repression_risk", 0, 10, line, &errors)
		checkRange(row, index, "free_rider_incentive", 0, 10, line, &errors)
		checkRange(row, index, "participation_intention", 0, 1, line, &errors)
		checkRange(row, index, "digital_engagement", 0, 10, line, &errors)
		checkRange(row, index, "offline_engagement", 0, 10, line, &errors)
		checkRange(row, index, "perceived_legitimacy", 0, 10, line, &errors)
		checkRange(row, index, "movement_outcome", 0, 10, line, &errors)
		checkRange(row, index, "response_time_ms", 150, 1000000, line, &errors)
		checkBinary(row, index, "action_participation", line, &errors)
	}

	fmt.Printf("Validated file: %s\n", path)
	fmt.Printf("Rows checked: %d\n", len(rows)-1)
	fmt.Printf("Validation errors: %d\n", errors)
	fmt.Println("Condition counts:")
	for condition, count := range conditionCounts {
		fmt.Printf("  %s: %d\n", condition, count)
	}
	fmt.Println("Domain counts:")
	for domain, count := range domainCounts {
		fmt.Printf("  %s: %d\n", domain, count)
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

func checkBinary(row []string, index map[string]int, col string, line int, errors *int) {
	value := row[index[col]]
	if value != "0" && value != "1" {
		fmt.Printf("Line %d: %s must be 0 or 1, got %s\n", line, col, value)
		*errors = *errors + 1
	}
}
