package main

import (
	"encoding/csv"
	"fmt"
	"log"
	"os"
	"strconv"
)

var required = []string{
	"participant","session_id","team_id","task_id","site_id","condition","task_type","trial",
	"group_size","solo_effort","group_effort","effort_loss","output_score","coordination_loss",
	"motivation_loss","identifiability","accountability","task_value","task_uniqueness",
	"task_visibility","perceived_dispensability","perceived_instrumentality","free_rider_expectation",
	"sucker_effect_concern","social_compensation_tendency","group_cohesion","group_identity_salience",
	"evaluation_potential","digital_traceability","remote_status","response_time_ms",
}

func main() {
	if len(os.Args) < 2 { log.Fatal("Usage: go run go/validator.go data/social_loafing_trials.csv") }
	f, err := os.Open(os.Args[1]); if err != nil { log.Fatal(err) }
	defer f.Close()
	rows, err := csv.NewReader(f).ReadAll(); if err != nil { log.Fatal(err) }
	if len(rows) < 2 { log.Fatal("CSV must contain header and at least one data row") }
	idx := map[string]int{}
	for i, h := range rows[0] { idx[h] = i }
	for _, col := range required {
		if _, ok := idx[col]; !ok { log.Fatalf("Missing column: %s", col) }
	}
	errors := 0
	counts := map[string]int{}
	for r, row := range rows[1:] {
		line := r + 2
		counts[row[idx["condition"]]]++
		check(row, idx, "trial", 1, 1000000, line, &errors)
		check(row, idx, "group_size", 1, 1000000, line, &errors)
		check(row, idx, "effort_loss", -100, 100, line, &errors)
		check(row, idx, "response_time_ms", 150, 1000000, line, &errors)
		for _, col := range []string{"solo_effort","group_effort","output_score","coordination_loss","motivation_loss"} {
			check(row, idx, col, 0, 100, line, &errors)
		}
		for _, col := range []string{"identifiability","accountability","task_value","task_uniqueness","task_visibility","perceived_dispensability","perceived_instrumentality","free_rider_expectation","sucker_effect_concern","social_compensation_tendency","group_cohesion","group_identity_salience","evaluation_potential","digital_traceability"} {
			check(row, idx, col, 0, 10, line, &errors)
		}
	}
	fmt.Printf("Validated: %s\nRows: %d\nErrors: %d\n", os.Args[1], len(rows)-1, errors)
	for k, v := range counts { fmt.Printf("%s: %d\n", k, v) }
	if errors > 0 { os.Exit(2) }
}

func check(row []string, idx map[string]int, col string, min float64, max float64, line int, errors *int) {
	v, err := strconv.ParseFloat(row[idx[col]], 64)
	if err != nil || v < min || v > max {
		fmt.Printf("Line %d: %s invalid or out of range [%.1f, %.1f]\n", line, col, min, max)
		*errors++
	}
}
