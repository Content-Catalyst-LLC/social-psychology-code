# Measurement Notes

## Bias

Bias = ObservedJudgment - NormativeBenchmark

## Anchoring error

AnchoringError = Estimate - TrueValue

## Anchor sensitivity

Estimate = beta0 + beta1*AnchorValue + beta2*TrueValue + error

A larger beta1 indicates stronger anchoring.

## Calibration error

CalibrationError = abs(ConfidenceRating - ActualAccuracy)

## Overconfidence

Overconfidence = ConfidenceRating - ActualAccuracy

## Base-rate neglect

BaseRateNeglect = RepresentativenessWeight - BaseRateWeight

## Affect-risk-benefit coupling

PerceivedRisk = alpha0 - alpha1*AffectValence + error
PerceivedBenefit = beta0 + beta1*AffectValence + error

## Framing effect

FrameEffect = MeanChoice(gain_frame) - MeanChoice(loss_frame)

## Decision quality

DecisionQuality = f(Accuracy, Calibration, EvidenceUse, Accountability, Feedback)

## Debiasing effect

DebiasingEffect = Bias_control - Bias_intervention

## Recommended validity checks

- Confirm that anchor values differ by condition.
- Confirm that availability salience manipulation affects recall ease.
- Confirm that framing changes presentation but not underlying expected value.
- Confirm that confidence and accuracy are measured on compatible scales.
- Test whether base-rate prompts reduce representativeness-driven error.
- Test whether accountability reduces anchoring or overconfidence.
- Test whether calibration feedback reduces overconfidence across trials.
