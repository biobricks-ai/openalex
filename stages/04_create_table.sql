-- Converted from https://github.com/ourresearch/openalex-documentation-scripts/blob/495ba3a626086d4dca4aa73f0fbb1c1cf69b0100/openalex-pg-schema.sql
-- using pg2sqlite after removing the schema prefix on table names.
-- Types added manually from the inferred parquet schema.

CREATE TABLE authors (id text, orcid text, display_name text, display_name_alternatives text, works_count int, cited_by_count int, last_known_institution text, works_api_url text, updated_date text);
CREATE TABLE authors_counts_by_year (author_id text, year int, works_count int, cited_by_count int, oa_works_count int);
CREATE TABLE authors_ids (author_id text, openalex text, orcid text, scopus text, twitter text, wikipedia text, mag real);
CREATE TABLE concepts (id text, wikidata text, display_name text, level int, description text, works_count int, cited_by_count int, image_url text, image_thumbnail_url text, works_api_url text, updated_date text);
CREATE TABLE concepts_ancestors (concept_id text, ancestor_id text);
CREATE TABLE concepts_counts_by_year (concept_id text, year int, works_count int, cited_by_count int, oa_works_count int);
CREATE TABLE concepts_ids (concept_id text, openalex text, wikidata text, wikipedia text, umls_aui text, umls_cui text, mag int);
CREATE TABLE concepts_related_concepts (concept_id text, related_concept_id text, score real);
CREATE TABLE institutions (id text, ror text, display_name text, country_code text, type text, homepage_url text, image_url text, image_thumbnail_url text, display_name_acronyms text, display_name_alternatives text, works_count int, cited_by_count int, works_api_url text, updated_date text);
CREATE TABLE institutions_associated_institutions (institution_id text, associated_institution_id text, relationship text);
CREATE TABLE institutions_counts_by_year (institution_id text, year int, works_count int, cited_by_count int, oa_works_count int);
CREATE TABLE institutions_geo (institution_id text, city text, geonames_city_id real, region text, country_code text, country text, latitude real, longitude real);
CREATE TABLE institutions_ids (institution_id text, openalex text, ror text, grid text, wikipedia text, wikidata text, mag real);
CREATE TABLE publishers (id text, display_name text, alternate_titles text, country_codes text, hierarchy_level int, parent_publisher text, works_count int, cited_by_count int, sources_api_url text, updated_date text);
CREATE TABLE publishers_counts_by_year (publisher_id text, year int, works_count int, cited_by_count int, oa_works_count int);
CREATE TABLE publishers_ids (publisher_id text, openalex text, ror text, wikidata text);
CREATE TABLE sources (id text, issn_l text, issn text, display_name text, publisher text, works_count int, cited_by_count int, is_oa int, is_in_doaj int, homepage_url text, works_api_url text, updated_date text);
CREATE TABLE sources_counts_by_year (source_id text, year int, works_count int, cited_by_count int, oa_works_count int);
CREATE TABLE sources_ids (source_id text, openalex text, issn_l text, issn text, mag real, wikidata text, fatcat text);
CREATE TABLE works (id text, doi text, title text, display_name text, publication_year int, publication_date text, type text, cited_by_count int, is_retracted int, is_paratext int, cited_by_api_url text, abstract_inverted_index text, language text);
CREATE TABLE works_primary_locations (work_id text, source_id text, landing_page_url text, pdf_url text, is_oa int, version text, license text);
CREATE TABLE works_locations (work_id text, source_id text, landing_page_url text, pdf_url text, is_oa int, version text, license text);
CREATE TABLE works_best_oa_locations (work_id text, source_id text, landing_page_url text, pdf_url text, is_oa int, version text, license text);
CREATE TABLE works_authorships (work_id text, author_position text, author_id text, institution_id text, raw_affiliation_string text);
CREATE TABLE works_biblio (work_id text, volume text, issue text, first_page text, last_page text);
CREATE TABLE works_concepts (work_id text, concept_id text, score real);
CREATE TABLE works_ids (work_id text, openalex text, doi text, mag real, pmid text, pmcid text);
CREATE TABLE works_mesh (work_id text, descriptor_ui text, descriptor_name text, qualifier_ui text, qualifier_name text, is_major_topic int);
CREATE TABLE works_open_access (work_id text, is_oa int, oa_status text, oa_url text, any_repository_has_fulltext int);
CREATE TABLE works_referenced_works (work_id text, referenced_work_id text);
CREATE TABLE works_related_works (work_id text, related_work_id text);
