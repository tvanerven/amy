# AMY Database structure

The primary tables used in AMY (that will appear in most queries) are those that store information on events, persons, memberships, and organizations.  Additional tables provide more information about events, persons, memberships, and organizations.  This information can be useful in writing [SQL queries in redash](https://redash.carpentries.org/queries).

## Primary Tables in AMY

### Events

`workshops_event` - Primary table for all event data.

#### Commonly used fields

* `id` Sequential, automatically assigned integer
* `start` and `end` Event start and end dates
* `slug` Event's unique identifier in the form YYYY-MM-DD-sitename
* `url` Event's website. Typically in the format username.github.io/YYYY-MM-DD-sitename (but not required)
* `host_id` An integer representing the Event Host.  This is linked to the `workshops_organization` table
* Location based fields:
    * `venue` The venue name of the event
    * `address` The street address of the event
    * `latitude` and `longitude` Stored as floating point (decimal) numbers
    * `country` Stored as the [two character country code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2)
* `contact` A list of email addresses listed as contacts for that workshop
* `completed` A Boolean field to note that all work (including workshop coordination and data entry) is complete.
* `assigned_to_id` The id of the Regional Coordinator or other Carpentries Core Team member assigned to this event. This is linked to the `workshops_person` table.
* `language_id` The integer id of the language used at the workshop. This is not typically recorded. This is linked to the `workshops_language` table
* `open_TTT_applications` Used only for instructor training events
* `adminstrator_id` An integer representing the event organizer.  This is linked to the `workshops_organization` table. Historically any organization could be listed as an administrator. Recent updates to AMY limit this to Data Carpentry, Library Carpentry, Software Carpentry, The Carpentries, or self-organized. This enforcement is at the AMY app level, not at the database level.
* `reg_key` Eventbrite registration key
* `instructors_pre` Link to both pre- and post-workshop survey results.

#### Unused fields

* `manual_attendance` We are no longer collecting or recording attendance
* `admin_fee`, `invoice_status` We are not recording financial data in AMY
* `repository_last_commit_hash`, `repository_metadata`, `metadata_all_changes`, `metadata_changed` Previously used to store metadata changes
* `instructors_post` `learners_longterm` `learners_post` `learners_pre` Previously used to store links to surveys.

### Persons

`workshops_person` - Primary table for all person data. This includes all individuals, regardless of their role with The Carpentries.

#### Commonly used fields

* `id` Sequential, automatically assigned integer
* `personal` `middle` `family` Three fields to hold the individual's name.  Only `personal` is required.
* `email` Individual's primary email address. Used for user log in
* `secondary_email` Alternate email address. Optional.
* `gender` Options are `Prefer not to say (undisclosed)` `Female` `Gender variant / non-conforming` `Male` `Other`.
    * `gender_other` Text if individual selected `Other`
* `may_contact` A boolean field. We may not contact people if this field is false. This field has been replaced by [new-style consents](#consent) (see also [2021 Consents Project](./design/projects/2021_consents.md)).
* `github` Individual's GitHub user id
* `twitter` Individual's Twitter user id
* `orcid` Individual's ORCID iD
* `url` Link to the individual's personal website
* `airport_id` An integer representing the person's self identified nearest.  This is linked to the `workshops_airport` table
* `affiliation` A free text field representing the person's self identified institutional affliation. This is **not** linked to the `workshops_organization` table.
* `occupation` A free text field representing the person's self identified occupation
* `user_notes` Free text field with notes from the individual
* `publish_profile` A boolean field that acknowledges permission to publish the individual's profile on our website pages such as the [Instructors](https://carpentries.org/instructors/), [Trainers](https://carpentries.org/trainers/), or [Maintainers](https://carpentries.org/maintainers/) pages. This field has been replaced by new-style consents.
* `country` Self identified country of residence. Stored as the [two character country code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2).
* `lesson_publication_consent` Allows individual to consent to publishing their name associated with lesson contributions. Individual can select publication by name, ORCID iD, or GitHub id, or not consent to publishing their name or identity. This field has been replaced by new-style consents.

#### Less commonly used fields

* `last_login` When the user last logged in (regardless of their activity or permissions)
* `is_superuser` Boolean field to note whether the person is a **superuser**, giving them all administrative privileges
* `created_at` Autogenerated timestamp when the record is created
* `last_updated_at` Autogenerated timestamp when the record was last updated
* `duplication_reviewed_on` Timestamp tracking when a [potential duplicate individual's record was reviewed](https://amy.carpentries.org/reports/duplicate_persons/)
* `is_active` A boolean field.  Only active users are able to log in to AMY
* `data_privacy_agreement` Acknowledges user has read our data policy. Required the first time any user logs in

#### Other fields

* `password` Not stored as plain text. Do not use or modify this field for anything.

### Memberships

`workshops_membership` - Stores information about each membership agreement.

* `id` Sequential, automatically assigned integer.
* `variant` Membership type (Gold, Silver, etc.)
* `agreement_start` and `agreement_end` Membership term start and end dates
* `extended` Integer; number of days the membership term end date has been extended by; `NULL` value indicates no extension
* `contribution_type` Financial, Person-days, or Other
* `workshops_without_admin_fee_per_agreement` Integer; number of centrally organized workshops allowed
* `workshops_without_admin_fee_rolled_from_previous` Integer; number of centrally-organised workshops allowed that was rolled over from previous membership. This should be the same as `workshops_without_admin_fee_rolled_over` in preceding membership
* `workshops_without_admin_fee_rolled_over` Integer; number of centrally-organised workshops allowed that was rolled over to succeeding membership. The same number should be recorded in `workshops_without_admin_fee_rolled_from_previous` in succeeding membership
* `public_instructor_training_seats` Integer; number of public seats allowed in instructor training events in the original contract.
* `additional_public_instructor_training_seats`  Integer; number of additional public seats allowed in instructor training events beyond the original contract.
* `public_instructor_training_seats_rolled_from_previous` Integer; number of public instructor training seats allowed that was rolled over from previous membership. This should be the same as `public_instructor_training_seats_rolled_over` in preceding membership
* `public_instructor_training_seats_rolled_over` Integer; number of public instructor training seats allowed that was rolled over to succeeding membership. The same number should be recorded in `public_instructor_training_seats_rolled_from_previous` in succeeding membership
* `inhouse_instructor_training_seats` Integer; number of in-house seats allowed in instructor training events in the original contract.
* `additional_inhouse_instructor_training_seats`  Integer; number of additional in-house seats allowed in instructor training events beyond the original contract.
* `inhouse_instructor_training_seats_rolled_from_previous` Integer; number of in-house instructor training seats allowed that was rolled over from previous membership. This should be the same as `inhouse_instructor_training_seats_rolled_over` in preceding membership
* `inhouse_instructor_training_seats_rolled_over` Integer; number of in-house instructor training seats allowed that was rolled over to succeeding membership. The same number should be recorded in `inhouse_instructor_training_seats_rolled_from_previous` in succeeding membership
* `agreement_link` A link to the Member agreement in Google Drive
* `registration_code` A string representing the code used by the Member site for Eventbrite registration and the instructor training application
* `public_status` a string indicating agreement to publicising membership on The Carpentries websites
* `emergency_contact` text with emergency contact data for the membership
* `consortium` a boolean value indicating consortium (umbrella for more than one organisation member)

### Member

`workshops_member` - Stores information about organisations and their roles in memberships.

* `id` Sequential, automatically assigned integer.
* `membership_id` - Integer linking membership instance
* `organization_id` - Integer linking organisation instance
* `role_id` - Integer linking member role instance

### MemberRole

`workshops_memberrole` - Stores roles for organisations in memberships.

* `id` Sequential, automatically assigned integer.
* `name` string with role's name, e.g. `contact_signatory` - preferably a computer-friendly format
* `verbose_name` string with role's name suitable for humans, e.g. `Contact Signatory`

### MembershipTask

`fiscal_membershiptask` - Stores information about persons and their roles in memberships.

* `id` Sequential, automatically assigned integer.
* `membership_id` - Integer linking membership instance
* `person_id` - Integer linking person instance
* `role_id` - Integer linking membership person role instance

### MembershipPersonRole

`fiscal_membershippersonrole` - Stores roles for persons in memberships.

* `id` Sequential, automatically assigned integer.
* `name` string with role's name - preferably a computer-friendly format
* `verbose_name` string with role's name suitable for humans


### Organizations

`workshops_organization` - Stores all organizations in AMY.

* `id` Sequential, automatically assigned integer.  This is used by the `host_id` and `administrator_id` fields in the `workshops_event` table, and the `organization_id` field in the `workshops_membership` table.
* `domain` Website of the organization
* `fullname` Human friendly name of the organization
* `country` Stored as the [two character country code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2)
* `latitude` and `longitude` Stored as floating point (decimal) numbers
* `affiliated_organizations` Many-to-many relationship between organizations; the purpose of this field is to "link together" organisations that in some way are related.
   For example, "University of California" organisation can be linked to "University of California, Berkeley", "University of California, Davis", and "University of California, Los Angeles".

## Additional Tables in AMY

### Badges

* `workshops_badge` Lists all available badges (Instructor, Trainer, etc.)
    * `id` Sequential, automatically assigned integer. This is used by `badge_id` in the `workshops_award` table.
    * `criteria` Description of what this badge is
    * `title` Verbose, human friendly name of badge (e.g., *Lesson Developer* or *Trainer*)
    * `name` "back-end" badge name (e.g., *lesson-developer*, *trainer*)

* `workshops_award` Connects `workshops_badge` and `workshops_person` tables to show what Badges have been awarded to what Persons
    * `id` Sequential, automatically assigned integer.
    * `awarded` Date the badge was awarded. This is usually the date it was recorded in AMY, not the date the person completed all requirements.
    * `badge_id` An integer representing the badge.  This is linked to the `workshops_badge` table
    * `event_id` An integer representing the event the badge came from.  This is linked to the `workshops_event` table
    * `person_id` An integer representing the person who got the badge.  This is linked to the `workshops_person` table
    * `awarded_by_id` An integer representing the person who awarded the badge (entered it in AMY).  This is linked to the `workshops_person` table

### Roles

* `workshops_role` Lists all available roles (Instructor, Helper, Learner, etc.)
    * `id`  Sequential, automatically assigned integer.
    * `verbose_name`  Verbose, human friendly name of role (e.g., *Workshop host*, *Supporting Instructor*)
    * `name`  "back end" task name (e.g., *workshop-host*, *supporting-instructor*)

* `workshops_task` Connects `workshops_role`, `workshops_event`, and `workshops_person` tables to show what what Persons have served in what Roles at what Events
    * `id`  Sequential, automatically assigned integer.
    * `event_id` An integer representing the event the person was at.  This is linked to the `workshops_event` table
    * `person_id` An integer representing the person who was at the event.  This is linked to the `workshops_person` table
    * `role_id` An integer representing the person's role.  This is linked to the `workshops_person` table
    * `seat_membership_id` Used for Instructor Training Learner role only.  An integer representing the membership this seat was assigned to.
    * `seat_public` Used for Instructor Training Learner role only.  Determines if the seat counts as public or in-house for the specific membership.
    * `seat_open_training` Used for Instructor Training Learner role only. Boolean field noting whether this was an open (non-member) training seat.
    * `title` and`url` are not used.

### Tags

* `workshops_tag` Lists all availabe tags for an Event (SWC, DC, LC, Online, Pilot, Circuits, etc.)
    * `id`  Sequential, automatically assigned integer.
    * `name`  "back end" tag name
    * `details` Description of what tag is used for
    * `priority` Used to control the sort order in the AMY web interface. Not relevant for any other queries.

* `workshops_event_tags` Connects `workshops_tag` and `workshops_event` to show what Tags have been applied to what Events
    * `id`  Sequential, automatically assigned integer.
    * `event_id` An integer representing the event that got that tag.  This is linked to the `workshops_event` table
    * `tag_id` An integer representing the tag that was assigned to that event.  This is linked to the `workshops_tag` table.


### Training progress

* `workshops_trainingrequirement`  Lists all available steps towards Instructor certification (Training Event, Welcome Session, etc.)
    * `id`  Sequential, automatically assigned integer.
    * `name` Name of requirement (*DC Homework*, *LC Demo*, etc.)
    * `url_required` Notes whether a URL is required for this type of training requirement.  This only applies to the *Lesson Contribution* requirements.
    * `event_required` Notes whether an event is required for this type of training requirement.  This only applies to the *Training* (the actual event they attended).

* `workshops_trainingprogress` Connects `workshops_trainingrequirement` and `workshops_person` to show what Persons have completed what steps of the checkout process.
    * `id`  Sequential, automatically assigned integer.
    * `created_at` and `last_updated_at`  Dates the record was created and last updated. Automatically generated by database.
    * `state` State of the trainee's progress.
        * `p`: pass
        * `a`: ask to repeat
        * `f`: fail
        * `n`: not evaluated yet
    * `url` Only for *Lesson Contribution* requirement; links to the trainee's GitHub contribution
    * `notes` Any human generated notes
    * `event_id` id of the event this trainee was at.  This is linked to the `workshops_event` table
    * `requirement_id` id of the requirement that is being recorded. This is linked to the `workshops_trainingrequirement` table
    * `trainee_id` id of the trainee being evaluated.  This is linked to the `workshops_person` table

### Term

`consents_term` - Stores all consent terms in AMY (e.g. privacy policy, permission to contact).

#### Archive Behavior

When a term is archived, that term's associated options and consents are archived as well. If the term was required, once archived it is no longer required in AMY.

#### Commonly used fields

* `slug` slug of the term. Used to uniquely identify the term.
* `content` content of the term. This text is shown to users when they consent.
* `training_request_content` if set, the regular `content` is replaced with this text when displaying this term on the instructor training request form.
* `required_type` determines whether or not a term is considered required for the user or not. If required it is presented to the user when they first log in.
* `help_text` additional text shown to the user in order to give more context on the term.
* `short_description` a short description of the consent, shown in the admin view of a profile
* `archived_at` if this term is archived, a timestamp of when it was archived

### TermOption

`consents_termoption` - Stores all options for all terms in AMY. Options are displayed when the user is asked to consent to a particular term. Options are considered answer choices for the term.

#### Archive Behavior

When an option is archived, any consents that rely on that option are archived and a new unset consent is created by AMY for the user. If the term the option was attached to is required, archiving the option may result in an email sent to any users who answered with this option.

#### Commonly used fields

* `term_id` id of the term this option belongs to. This is linked to the `consents_term` table. Unarchived term options attached to a term will be displayed to the user when the term is rendered.
* `option_type` determines whether or not a term option is considered as an agreement or a decline for that term.
* `content` the text displayed to the user when the term is rendered.
* `archived_at` a timestamp of when the option was archived or `NULL` if it wasn't

### Consent

`consents_consent` - Stores all consents for all users in AMY.

#### Archive Behavior

When consents are archived, a new unset consent is created by AMY for each term involved.

#### Commonly used fields

* `person_id` id of the person providing the consent. This is linked to the `workshops_person` table.
* `term_id` id of the term this consent applies to. This is linked to the `consents_term` table. There is a check on the Consent model to ensure the given TermOption belongs to the Term.
* `term_option_id` id of the term option chosen in this consent. This is linked to the `consents_termoption` table. When this field is null, the consent has not been set by the user.
* `archived_at` if this consent is archived, a timestamp of when it was archived.

### TrainingRequestConsent

`consents_trainingrequestconsent` Stores all consents for all instructor training requests in AMY.

#### Archive Behavior

When training request consents are archived, a new unset consent is created by AMY for each term involved.

#### Commonly used fields

* `training_request_id` id of the training request this consent option belongs to. This is linked to the `workshops_trainingrequest` table.
* `term_id` id of the term this consent applies to. This is linked to the `consents_term` table. There is a check on the Consent model to ensure the given TermOption belongs to the Term.
* `term_option_id` id of the term option chosen in this consent. This is linked to the `consents_termoption` table. When this field is null, the consent has not been set by the user.
* `archived_at` a timestamp of when the consent was archived or `NULL` if it wasn't.