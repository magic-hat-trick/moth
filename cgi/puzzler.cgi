#! /usr/bin/lua

local cgi = require "cgi"
local koth = require "koth"

local team = cgi.fields['t'] or ""
local category = cgi.fields['c'] or ""
local points = cgi.fields['p'] or ""
local answer = cgi.fields['a'] or ""

-- Defang category name; prevent directory traversal
category = category:gsub("[^A-Za-z0-9]", "-")

-- Check answer
local needle = points .. " " .. answer
local haystack = "../puzzles/" .. category .. "/answers.txt"
local found = koth.anchored_search(haystack, needle)

if (not found) then
	koth.page("Wrong answer")
end

local ok = koth.award_points(team, category, points, "P");
if (not ok) then
	koth.page("Error awarding points", "You got the right answer, but something blew up trying to give you points. Try again in a few seconds.")
end

koth.page("Points awarded",
	"<p>" .. points .. " points for " .. team .. ".</p>" ..
	"<p><a href=\"puzzles.html\">Back to puzzles</a></p>")
